"""Production settings for Render deployment."""
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from .base import *

# In production, DEBUG must strictly be False
DEBUG = False

# Production requires an explicit, strong SECRET_KEY
SECRET_KEY = config('SECRET_KEY', default='')
if not SECRET_KEY or SECRET_KEY.startswith('django-insecure-') or len(SECRET_KEY) < 32:
    raise ImproperlyConfigured(
        "Production requires a strong, unique SECRET_KEY environment variable "
        "(at least 32 characters, and not using the 'django-insecure-' prefix). "
        "Generate one using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
    )

# Production requires ALLOWED_HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ImproperlyConfigured(
        "Production requires ALLOWED_HOSTS environment variable "
        "(e.g. ALLOWED_HOSTS=your-app.onrender.com)."
    )

# Production requires CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())
if not CSRF_TRUSTED_ORIGINS or CSRF_TRUSTED_ORIGINS == ['']:
    raise ImproperlyConfigured(
        "Production requires CSRF_TRUSTED_ORIGINS environment variable "
        "(e.g. CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com)."
    )

# Production requires a valid DATABASE_URL (no silent SQLite fallback)
DATABASE_URL = config('DATABASE_URL', default=None)
if not DATABASE_URL:
    raise ImproperlyConfigured(
        "Production requires a valid DATABASE_URL environment variable (e.g. PostgreSQL). "
        "SQLite cannot be used in production because Render uses an ephemeral filesystem."
    )

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=config('DB_SSL_REQUIRE', default=True, cast=bool),
    )
}

# HTTPS & Proxy Configuration (Render reverse proxy compatibility)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Persistent Media Storage: AWS S3 / Cloudflare R2 / S3-compatible via django-storages
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default=None)
ALLOW_EPHEMERAL_MEDIA = config('ALLOW_EPHEMERAL_MEDIA', default=False, cast=bool)
SERVE_MEDIA_LOCAL = config('SERVE_MEDIA_LOCAL', default=False, cast=bool)

if AWS_STORAGE_BUCKET_NAME:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ImproperlyConfigured(
            "When AWS_STORAGE_BUCKET_NAME is configured, AWS_ACCESS_KEY_ID and "
            "AWS_SECRET_ACCESS_KEY must also be provided."
        )

    if 'storages' not in INSTALLED_APPS:
        INSTALLED_APPS.append('storages')

    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=None)  # Cloudflare R2 / MinIO
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False

    STORAGES = {
        **STORAGES,
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        },
    }

    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    elif AWS_S3_ENDPOINT_URL:
        MEDIA_URL = f"{AWS_S3_ENDPOINT_URL.rstrip('/')}/{AWS_STORAGE_BUCKET_NAME}/"
    else:
        MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/'
elif not ALLOW_EPHEMERAL_MEDIA and not SERVE_MEDIA_LOCAL:
    raise ImproperlyConfigured(
        "Production requires persistent media storage configuration (AWS_STORAGE_BUCKET_NAME, "
        "AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) because Render uses an ephemeral filesystem. "
        "To explicitly bypass this requirement for testing, set ALLOW_EPHEMERAL_MEDIA=True."
    )

# Email (configure with SendGrid, Mailgun, or standard SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
