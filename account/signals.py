
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from .models import *
import requests
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import uuid

User = get_user_model()

import logging

logger = logging.getLogger(__name__)


def generate_referral_code():
    code = str(uuid.uuid4()).replace("-", "")[:7]
    return code


@receiver(post_save, sender=User)
def customer_Profile(sender, instance, created, *args, **kwargs):
    if created:
        # Ensure the necessary groups are created
        free_group, created = Group.objects.get_or_create(name='Free')
        
        # Add the user to the "Free" group by default
        instance.groups.add(free_group)

        UserProfile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            referral_code = generate_referral_code()
        )
        

        

@receiver(post_save, sender=User)
def update_Profile(sender, instance, created, *args, **kwargs):
    if not created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        if created:
            print('User Profile was missing and has been created for existing user')
        else:
            profile.save()
            





@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if not created and instance.is_verified and not instance._state.adding:
        context = {
            'get_full_name': instance.get_full_name,
            'email': instance.email
        }

        subject = 'Welcome to Bitphyte Limited'
        text_content = render_to_string('email/welcome_email.txt', context)
        html_content = render_to_string('email/welcome_email.html', context)

        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
                auth=("api", settings.MAILGUN_API_KEY),
                data={
                    "from": f"Bitphyte <{settings.DEFAULT_FROM_EMAIL}>",
                    "to": [instance.email],
                    "subject": subject,
                    "text": text_content,
                    "html": html_content
                }
            )
            response.raise_for_status()
            logger.info(f"Welcome email sent to {instance.email}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send welcome email to {instance.email}: {str(e)}")










@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        logger.info("Password reset signal triggered.")

        user = reset_password_token.user
        custom_url_base = "https://www.bitphyte.com/reset_password_confirm"
        reset_url = f"{custom_url_base}?token={reset_password_token.key}"

        context = {
            "first_name": user.first_name,
            "reset_password_url": reset_url,
            "site_name": "bitphyte.com",
            "support_email": "support@bitphyte.com"
        }

        subject = "Password Reset for Bitphyte"
        text_content = render_to_string("email/user_reset_password.txt", context)
        html_content = render_to_string("email/user_reset_password.html", context)

        response = requests.post(
            f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": f"Bitphyte <{settings.DEFAULT_FROM_EMAIL}>",
                "to": [user.email],
                "subject": subject,
                "text": text_content,
                "html": html_content
            }
        )
        response.raise_for_status()
        logger.info(f"Password reset email sent to {user.email}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending password reset email to {user.email}: {str(e)}")
