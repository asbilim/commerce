# apps/users/signals.py

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import User

# This signal runs when email is confirmed
@receiver(email_confirmed)
def handle_email_confirmation(sender, request, email_address, **kwargs):
    """
    When email is confirmed:
    1. Set user as verified
    2. Send welcome email
    """
    user = email_address.user
    if not user.is_verified:
        user.is_verified = True
        user.save()
        
        # Send welcome email
        send_welcome_email(user)


def send_welcome_email(user):
    """Centralized welcome email function"""
    subject = 'Welcome to Our Platform!'
    context = {
        'user': user,
        'site_name': 'Your Site Name'
    }
    
    html_message = render_to_string('account/email/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )