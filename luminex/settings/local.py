"""Local development settings."""
from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend for development - print to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use standard StaticFilesStorage in development to prevent missing manifest errors during tests
STORAGES = {
    **STORAGES,
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

