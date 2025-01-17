import logging
from typing import Optional, Dict, Any, Union
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.core.mail.backends.smtp import EmailBackend
from smtplib import SMTPException

logger = logging.getLogger(__name__)

class CustomEmailBackend(EmailBackend):
    """Custom Email Backend with enhanced debugging"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'connection'):
            self.connection.set_debuglevel(1)

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for handling Allauth email operations with enhanced
    functionality, logging, and error handling.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        
    def format_email_subject(self, subject: str) -> str:
        """
        Format the email subject with a prefix if configured
        """
        prefix = getattr(settings, 'ACCOUNT_EMAIL_SUBJECT_PREFIX', '')
        return f"{prefix}{subject}" if prefix else subject

    def get_from_email(self) -> str:
        """
        Get the from email address with fallbacks
        """
        return getattr(
            settings,
            'ACCOUNT_EMAIL_FROM',
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost')
        )

    def render_mail(
        self,
        template_prefix: str,
        email: str,
        context: Dict[str, Any],
        headers: Optional[Dict[str, Any]] = None
    ) -> Union[EmailMessage, EmailMultiAlternatives]:
        """
        Renders an email using templates with enhanced logging and customization
        """
        try:
            # Get the subject
            subject = self.format_email_subject(
                render_to_string(f'{template_prefix}_subject.txt', context)
            ).strip()

            # Render both text and HTML versions
            text_body = render_to_string(f'{template_prefix}_message.txt', context)
            html_body = render_to_string(f'{template_prefix}_message.html', context)

            # Log the email content for debugging
            self.logger.debug(f"Rendering email for {email}")
            self.logger.debug(f"Subject: {subject}")
            self.logger.debug(f"Template prefix: {template_prefix}")

            # Create the email message
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=self.get_from_email(),
                to=[email],
                headers=headers or {}
            )

            # Attach HTML version
            if html_body:
                msg.attach_alternative(html_body, "text/html")

            return msg

        except Exception as e:
            self.logger.error(f"Error rendering email: {str(e)}", exc_info=True)
            raise

    def send_mail(self, template_prefix: str, email: str, context: Dict[str, Any]) -> None:
        """
        Send an email with enhanced error handling and logging
        """
        try:
            # Add additional context data if needed
            context.update({
                'site_name': getattr(settings, 'SITE_NAME', 'Your Site'),
                'site_domain': getattr(settings, 'SITE_DOMAIN', 'example.com'),
            })

            # Render and prepare the email
            msg = self.render_mail(template_prefix, email, context)

            # Log the email attempt
            self.logger.info(f"Attempting to send email to {email}")
            self.logger.debug(f"Email details: From={msg.from_email}, To={msg.to}")

            # Send the email
            msg.send()

            # Log success
            self.logger.info(f"Successfully sent email to {email}")

        except SMTPException as e:
            self.logger.error(f"SMTP error sending email to {email}: {str(e)}")
            self.logger.error(f"SMTP Response: {getattr(e, 'smtp_error', 'No SMTP error details')}")
            self.logger.error(f"SMTP Code: {getattr(e, 'smtp_code', 'No SMTP code')}")
            raise

        except Exception as e:
            self.logger.error(f"Error sending email to {email}: {str(e)}", exc_info=True)
            raise

    def validate_unique_email(self, email: str) -> None:
        """
        Override to customize unique email validation if needed
        """
        try:
            super().validate_unique_email(email)
        except Exception as e:
            self.logger.error(f"Email validation error for {email}: {str(e)}")
            raise