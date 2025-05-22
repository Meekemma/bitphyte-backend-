from rest_framework import serializers
from .models import *
from account.models import UserProfile
from datetime import timedelta
from django.utils import timezone




class ReferralSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, required=True)  
    referee_count = serializers.SerializerMethodField()
    referral_bonus = serializers.SerializerMethodField()
    referee_details = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = [
            'code', 'referee', 'referrer', 'status', 'bonus', 'referred_at',
            'referee_count', 'referral_bonus', 'referee_details'
        ]
        read_only_fields = [
            'referee', 'referrer', 'status', 'bonus', 'referred_at',
            'referee_count', 'referral_bonus', 'referees'
        ]

    def get_referee_count(self, obj):
        if not obj.referrer:
            return 0
        return Referral.get_referee_count(obj.referrer)

    def get_referral_bonus(self, obj):
        if not obj.referrer:
            return 0.00
        return Referral.get_referral_bonus(obj.referrer)

    def get_referee_details(self, obj):
        # Return details for the specific referee of this referral
        if not obj.referee:
            return {}
        return {
            'email': obj.referee.user.email,
            'full_name': f"{obj.referee.user.first_name} {obj.referee.user.last_name}",
            'status': obj.status,
            'bonus': obj.bonus,
            'referred_at': obj.referred_at,
        }


    def validate_code(self, value):
        try:
            referrer_profile = UserProfile.objects.get(referral_code=value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("This referral code does not exist.")
        
        self.context['referrer_profile'] = referrer_profile
        return value

    def create(self, validated_data):
        referrer_profile = self.context.get('referrer_profile')
        referee_profile = self.context.get('referee_profile')

        if referee_profile == referrer_profile:
            raise serializers.ValidationError("You cannot refer yourself.")

        if Referral.objects.filter(referee=referee_profile).exists():
            raise serializers.ValidationError("This user has already been referred.")

        referral = Referral.objects.create(
            code=validated_data['code'],
            referrer=referrer_profile,
            referee=referee_profile,
            status='pending',
            bonus=0.00,
        )
        return referral
    





class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'subscribed_at', 'is_active']
        read_only_fields = ['subscribed_at', 'is_active']

    def validate_email(self, value):
       
        subscriber = Subscriber.objects.filter(email__iexact=value).first()
        if subscriber:
            if subscriber.is_active:
                raise serializers.ValidationError("This email is already subscribed.")
            else:
                
                return value
        return value

    def create(self, validated_data):
        # Normalize email to lowercase
        validated_data['email'] = validated_data['email'].lower()

        # Check for existing subscriber (case-insensitive)
        subscriber = Subscriber.objects.filter(email__iexact=validated_data['email']).first()
        
        if subscriber:
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save()
            return subscriber
        else:
            return Subscriber.objects.create(**validated_data)
        






class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Name cannot contain numbers.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        if len(value.strip()) < 250:
            raise serializers.ValidationError("Message must be at least 250 characters long.")
        return value

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)




