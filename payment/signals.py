from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Balance

@receiver(post_save, sender=Payment)
def update_user_balance(sender, instance, created, update_fields=None, **kwargs):
    """
    Update user's balance only when a payment is marked as completed and verified.
    Triggers on payment creation or status update.
    """
    if instance.status == "completed" and instance.verified_by_admin:
        balance, _ = Balance.objects.get_or_create(user=instance.user)
        balance.update_balance()
