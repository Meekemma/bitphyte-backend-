from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from .models import Subscriber
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








@receiver(post_save, sender=Subscriber, dispatch_uid="handle_subscription_email")
def handle_subscription_status(sender, instance, created, **kwargs):
    """
    Send email on subscription or unsubscription.
    """
    # Base context
    context = {
        'email': instance.email,
    }

    if created and instance.is_active:
        # Subscription flow
        unsubscribe_link = f"{settings.BASE_URL}{reverse('unsubscribe', kwargs={'email': instance.email})}"
        context['unsubscribe_link'] = unsubscribe_link
        subject = "Successful Newsletter Subscription"
        template_txt = 'email/subscription_email.txt'
        template_html = 'email/subscription_email.html'
    elif not created and not instance.is_active:
        # Unsubscription flow
        subject = "You Have Unsubscribed from Our Newsletter"
        template_txt = 'email/unsubscription_email.txt'
        template_html = 'email/unsubscription_email.html'
    else:
        return  # No action needed

    # Render email content
    text_content = render_to_string(template_txt, context)
    html_content = render_to_string(template_html, context)

    # Compose email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[instance.email],
    )
    email.attach_alternative(html_content, "text/html")

    # Add Postmark stream header
    email.extra_headers = {'X-PM-Message-Stream': 'outbound'}

    # Send
    email.send(fail_silently=False)
