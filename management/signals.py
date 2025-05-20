from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model() 
from account.models import UserProfile
from .models import Referral


@receiver(post_save, sender=User)
def reward_referrer_after_verification(sender, instance, created, **kwargs):
    """
    Trigger referral bonus once user verifies their email.
    """
    if created:
        return 

    # Only proceed if the user just became verified
    if instance.is_verified:
        try:
            referee_profile = UserProfile.objects.get(user=instance)
            referral = Referral.objects.get(referee=referee_profile, status='pending')
            
            referral.status = 'earned'
            referral.bonus = 10.00 
            referral.save()

            print(f"Referral bonus granted to {referral.referrer} for verified referee {referral.referee}")

        except (UserProfile.DoesNotExist, Referral.DoesNotExist):
            # No referral or profile exists — nothing to do
            pass