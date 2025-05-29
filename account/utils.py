import secrets
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from .models import User, OneTimePassword
import logging

logger = logging.getLogger(__name__)



def generate_otp():
    """Generate a cryptographically secure 6-digit OTP."""
    return ''.join(secrets.choice('0123456789') for _ in range(6))



def send_code_to_user(email):
    """Send OTP to user's email."""
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return {"status": "error", "message": "User does not exist"}

    if user.is_verified:
        return {"status": "error", "message": "User already verified"}

    # Generate OTP
    otp_code = generate_otp()

    # Update or create OTP (handles OneToOneField)
    try:
        OneTimePassword.objects.update_or_create(
            user=user,
            defaults={'code': otp_code, 'created_at': timezone.now()}
        )
    except Exception as e:
        logger.error(f"Failed to save OTP for {email}: {str(e)}")
        return {"status": "error", "message": "Failed to save OTP"}

    # Email context
    current_site = "Trexiz.com"
    email_subject = "Verify your email with this OTP"
    context = {
        "first_name": user.first_name,
        "otp_code": otp_code,
        "site_name": current_site,
        "support_email": "support@trexiz.com"
    }

    # Render email templates
    text_content = render_to_string("email/otp_mail.txt", context)
    html_content = render_to_string("email/otp_mail.html", context)

    # Send email
    try:
        email = EmailMultiAlternatives(
            subject=email_subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        
        email.send(fail_silently=False)
        return {"status": "success", "message": "OTP sent successfully"}
    except Exception as e:
        logger.error(f"Failed to send OTP to {email}: {str(e)}")
        return {"status": "error", "message": "Failed to send OTP"}


