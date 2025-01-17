import os
from pathlib import Path
from dotenv import load_dotenv
from .unfold import *
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'Du*^(RlkequrVXbOx4VfICSW$cNqVY_wrGyct_Z3C%CE7n9(sR')

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'rest_framework',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth.registration',
    'core',
    'django_extensions',
    'corsheaders',
    'storages',
    'import_export',
    'rangefilter',
    'mptt',
    'taggit',
    'apps.users', # we'll add more as we go
    'drf_spectacular',
]

TAGGIT_CASE_INSENSITIVE = True

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
     'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3005',
    'http://127.0.0.1:3001',
    'http://127.0.0.1:3000',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
# For local dev, media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


AUTH_USER_MODEL = 'users.User'


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# DRF basic settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


SITE_ID = 1
REST_USE_JWT = True  #
JWT_AUTH_COOKIE = 'auth'
JWT_AUTH_REFRESH_COOKIE = 'refresh'

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # or 'optional' or 'none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# These settings might help with debugging
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Commerce "
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"  # or "https" depending on your setup

AUTHENTICATION_BACKENDS = [
    # Default Django backend
    'django.contrib.auth.backends.ModelBackend',
    # AllAuth specific authentication methods
    'allauth.account.auth_backends.AuthenticationBackend',
]

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'



# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'wednesday.mxrouting.net')  # or your SMTP server
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)  # Common ports: 587 (TLS) or 465 (SSL)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER','commerce@devsplug.com')  # Your email address
EMAIL_HOST_COMMERCE_PASSWORD = os.getenv('EMAIL_HOST_COMMERCE_PASSWORD')  # Your email password or app-specific password
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'commerce@devsplug.com')

# Optional email settings
EMAIL_TIMEOUT = 30  # Timeout in seconds
EMAIL_SUBJECT_PREFIX = '[Commerce Notification] '  # Prefix for email subjects


ACCOUNT_ADAPTER ='config.adapters.accounts.CustomAccountAdapter'
