from rest_framework import serializers
from .models import Referral
from account.models import UserProfile




class ReferralSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, required=True)  
    referee_count = serializers.SerializerMethodField()
    referral_bonus = serializers.SerializerMethodField()
    referees = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = [
            'code', 'referee', 'referrer', 'status', 'bonus', 'referred_at',
            'referee_count', 'referral_bonus', 'referees'
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
    
    def get_referees(self, obj):
        if not obj.referrer:
            return []
        referees = Referral.get_referees(obj.referrer)
        return [
            {
                'email': r.referee.user.email,
                'full_name': f"{r.referee.user.first_name} {r.referee.user.last_name}",
                'status': r.status,
                'bonus': r.bonus,
                'referred_at': r.referred_at,
            }
            for r in referees
        ]

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
