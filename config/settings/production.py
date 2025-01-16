from .base import *
from dotenv import load_dotenv


load_dotenv()

DEBUG = False
ALLOWED_HOSTS = ['*']


# Secure settings, logging, etc.


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')

# Instead of the standard AWS endpoint, use R2's endpoint.
AWS_S3_ENDPOINT_URL = os.getenv('CLOUDFLARE_R2_ENDPOINT_URL')

# For R2, region is often set to "auto" or an empty string, 
# but you can use an env var if needed:
AWS_S3_REGION_NAME = os.getenv('CLOUDFLARE_R2_REGION', 'auto')

# Make sure Boto3 knows it’s a custom endpoint (necessary for R2).
AWS_S3_CUSTOM_DOMAIN = None

# If you need to override signature version, you can do:
# AWS_S3_SIGNATURE_VERSION = 's3v4'

# Example: If you want public read on uploaded files (be careful with this!):
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False  # if you don't want querystring tokens

# Other security / caching / etc. can be configured similarly.