import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'change_me_in_production')

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'apps.users', # we'll add more as we go
    'django_extensions',
    'corsheaders',
    'storages'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
     'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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
        'DIRS': [],
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

# DRF basic settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')


#unfold admin

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Commercial Admin",  # Title in the browser tab
    "SITE_HEADER": "Commercial Dashboard",  # Sidebar header title
    "SITE_URL": "/",  # Link for "View Site" button
    "SITE_ICON": {
        "light": lambda request: "https://cdn-icons-png.flaticon.com/512/833/833314.png",  # General business icon
        "dark": lambda request: "https://cdn-icons-png.flaticon.com/512/833/833316.png",
    },
    "SITE_LOGO": {
        "light": lambda request: "https://via.placeholder.com/150x50?text=Commercial+Light",  # Replace with a light logo
        "dark": lambda request: "https://via.placeholder.com/150x50?text=Commercial+Dark",   # Replace with a dark logo
    },
    "SITE_SYMBOL": "business",  # Material symbol
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: "https://cdn-icons-png.flaticon.com/512/833/833314.png",
        },
    ],
    "SHOW_HISTORY": True,  # Enable history tracking in admin
    "SHOW_VIEW_ON_SITE": True,  # Enable "View on Site" button
    "ENVIRONMENT": "config.environment_callback",  # Dynamically determine environment
    "THEME": None,  # Default theme with light/dark switcher
    "LOGIN": {
        "image": lambda request: "https://via.placeholder.com/1920x1080?text=Welcome+to+Commercial",  # Background for login page
        "redirect_after": lambda request: reverse_lazy("admin:index"),  # Redirect after login
    },
    "STYLES": [
        lambda request: "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",  # Include FontAwesome
    ],
    "SCRIPTS": [
        lambda request: "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js",  # Example JS library for charts
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "EXTENSIONS": {},
    "SIDEBAR": {
        "show_search": True,  # Enable search
        "show_all_applications": True,  # Enable dropdown for all apps
        "navigation": [
            {
                "title": _("Main Navigation"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [],
}
