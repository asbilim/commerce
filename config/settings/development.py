from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']


# Example: override DB if using Postgres locally
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'my_db',
#         'USER': 'my_user',
#         'PASSWORD': 'my_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
