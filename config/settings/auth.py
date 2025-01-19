import os

class AuthenticationConfig:
    """Centralized authentication configuration management"""
    
    @classmethod
    def get_settings(cls):
        """
        Returns a dictionary of all authentication-related settings
        """
        return {
       
            'FRONTEND': {
                'BASE_URL': os.getenv('WEBSITE_FRONTEND_URL', 'http://localhost:3000'),
                'SUCCESS_REDIRECT': '/email-verified',
                'ERROR_REDIRECT': '/email-verification-failed',
                'LOGIN_REDIRECT': '/dashboard',
            },
            'EMAIL': {
                'VERIFICATION_TEMPLATE': 'account/email/email_confirmation.html',
                'WELCOME_TEMPLATE': 'account/email/welcome.html',
                'CONFIRMATION_EXPIRE_DAYS': 3,
            },
        }