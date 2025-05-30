import secrets
import requests
import logging
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from .models import User, OneTimePassword

logger = logging.getLogger(__name__)


def generate_otp():
    """Generate a cryptographically secure 6-digit OTP."""
    return ''.join(secrets.choice('0123456789') for _ in range(6))


def send_code_to_user(email):
    """Send OTP to user's email via Mailgun API."""
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return {"status": "error", "message": "User does not exist"}

    if user.is_verified:
        return {"status": "error", "message": "User already verified"}

    # Generate OTP
    otp_code = generate_otp()

    # Save or update OTP
    try:
        OneTimePassword.objects.update_or_create(
            user=user,
            defaults={'code': otp_code, 'created_at': timezone.now()}
        )
    except Exception as e:
        logger.error(f"Failed to save OTP for {email}: {str(e)}")
        return {"status": "error", "message": "Failed to save OTP"}

    # Email content
    current_site = "Bitphyte.com"
    email_subject = "Verify your email with this OTP"
    context = {
        "first_name": user.first_name,
        "otp_code": otp_code,
        "site_name": current_site,
        "support_email": "support@bitphyte.com"
    }

    text_content = render_to_string("email/otp_mail.txt", context)
    html_content = render_to_string("email/otp_mail.html", context)

    # Send via Mailgun
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": f"Bitphyte <{settings.DEFAULT_FROM_EMAIL}>",
                "to": [user.email],
                "subject": email_subject,
                "text": text_content,
                "html": html_content,
            }
        )
        response.raise_for_status()
        return {"status": "success", "message": "OTP sent successfully"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send OTP to {email} via Mailgun: {str(e)}")
        return {"status": "error", "message": "Failed to send OTP"}
