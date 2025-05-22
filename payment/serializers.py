from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import WithdrawalRequest, Balance, Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'plan', 'amount_paid',
            'currency', 'transaction_id', 'status', 'created_at'
        ]
        read_only_fields = ['transaction_id', 'status', 'created_at']

    # Ensure amount is positive and greater than zero
    def validate_amount_paid(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount paid must be greater than zero.")
        return value

    # Validate plan against allowed choices
    def validate_plan(self, value):
        if value not in dict(Payment.PLAN_CHOICES):
            raise serializers.ValidationError("Invalid plan selected.")
        return value

    # Validate currency against allowed choices
    def validate_currency(self, value):
        if value not in dict(Payment.CURRENCY_CHOICES):
            raise serializers.ValidationError("Invalid currency selected.")
        return value

    # Cross-field validation based on selected plan and amount
    def validate(self, data):
        plan = data.get('plan')
        amount = data.get('amount_paid')

        # Plan-specific amount limits
        if plan == 'starter':
            if amount < 100:
                raise serializers.ValidationError("Minimum amount for the Starter plan is 100.")
            if amount > 1000:
                raise serializers.ValidationError("Maximum amount for the Starter plan is 1000.")

        elif plan == 'standard':
            if amount <= 1000:
                raise serializers.ValidationError("Minimum amount for the Standard plan must be above 1000.")
            if amount > 10000:
                raise serializers.ValidationError("Maximum amount for the Standard plan is 10000.")

        elif plan == 'advanced':
            if amount <= 10000:
                raise serializers.ValidationError("Minimum amount for the Advanced plan must be above 10000.")
            if amount > 1000000:
                raise serializers.ValidationError("Maximum amount for the Advanced plan is 1000000.")
        
        return data

    # Automatically attach the authenticated user to the payment creation
    # This method is called when creating a new payment
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return Payment.objects.create(**validated_data)
