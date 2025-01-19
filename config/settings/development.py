# config/development.py

from .base import *

# --------------------------------------------------------------------------
# DEBUG SETTINGS
# --------------------------------------------------------------------------
DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ['*']

# --------------------------------------------------------------------------
# INSTALLED APPS
# --------------------------------------------------------------------------
# Add development-specific apps
INSTALLED_APPS += [
    'debug_toolbar',
]

# --------------------------------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------------------------------
# Insert Debug Toolbar middleware at the top
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# --------------------------------------------------------------------------
# INTERNAL IPS (Required for Debug Toolbar)
# --------------------------------------------------------------------------
# Define internal IPs for Django Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# --------------------------------------------------------------------------
# DEBUG TOOLBAR CONFIGURATION
# --------------------------------------------------------------------------
# Optional: Customize Debug Toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'INTERCEPT_REDIRECTS': False,
}

# --------------------------------------------------------------------------
# STATIC FILES (Optional)
# --------------------------------------------------------------------------
# Optional: Override static files settings if needed
# STATICFILES_DIRS = [BASE_DIR / 'static_dev']

# --------------------------------------------------------------------------
# MEDIA FILES
# --------------------------------------------------------------------------
# Use Cloudflare R2 for media storage in development
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS S3 (Cloudflare R2) Configuration
AWS_ACCESS_KEY_ID = os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('CLOUDFLARE_R2_ENDPOINT_URL')
AWS_S3_REGION_NAME = os.getenv('CLOUDFLARE_R2_REGION', 'auto')
AWS_S3_CUSTOM_DOMAIN = None  # Optional: Set if using a custom domain
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False  # Disable querystring tokens for public access

# --------------------------------------------------------------------------
# EMAIL SETTINGS
# --------------------------------------------------------------------------
# Override email backend to use console during development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --------------------------------------------------------------------------
# CACHING (Optional)
# --------------------------------------------------------------------------
# Optional: Configure caching for development
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }

# --------------------------------------------------------------------------
# LOGGING (Optional)
# --------------------------------------------------------------------------
# Optional: Configure logging for development
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'DEBUG',
#     },
# }


DEBUG_TOOLBAR_CONFIG['IS_RUNNING_TESTS'] = False