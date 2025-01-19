# apps/users/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from allauth.socialaccount.helpers import ImmediateHttpResponse
from django.shortcuts import redirect
import logging
from datetime import datetime
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # If there's already a social account linked, `sociallogin.is_existing` is True.
        # The default flows might raise `assert not sociallogin.is_existing`.
        # We skip the parent logic in that case to avoid the crash.
        
        if sociallogin.is_existing:
            # Option A: Simply do nothing, let allauth proceed to log them in.
            # return

            return

        # If it's a new social signup, call the parent which triggers the normal flow:
        return super().pre_social_login(request, sociallogin)

    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.
        """
        user = super().populate_user(request, sociallogin, data)
        user.is_verified = True
        return user
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # Mark them as verified or send welcome email if new:
        if not sociallogin.is_existing:
            # e.g. user.is_verified = True
            self.send_welcome_email(user)
            pass

        return user
    


    def send_welcome_email(self, user):
        """
        Sends a welcome email to the newly registered user.
        """
        subject = 'Welcome to Our Platform!'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        # Context for the email template
        context = {
            'user': user,
            'current_year': datetime.now().year,
        }

        try:
            # Render the HTML template
            html_content = render_to_string('account/email/welcome.html', context)

            # Create the email message
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=from_email,
                to=[to_email],
            )
            email.content_subtype = 'html'  # Set the content subtype to HTML

            # Send the email
            email.send(fail_silently=False)
            logger.info(f"Welcome email sent to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {e}")

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Constructs the email confirmation (activation) url.
        """
        return f"{settings.WEBSITE_FRONTEND_URL}/auth/verify-email/{emailconfirmation.key}" 


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Constructs the email confirmation (activation) url.
        """
        return f"{settings.WEBSITE_FRONTEND_URL}/auth/verify-email/{emailconfirmation.key}"