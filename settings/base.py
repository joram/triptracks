import os
from settings.default import *

DEBUG = True

BASE_DIR = os.path.normpath(os.path.join(os.path.abspath(__file__), "../../.."))

# MUST OVERRIDE
DATABASES = {}


ALLOWED_HOSTS = [
    'triptracks.herokuapp.com',
    'localhost',
]

INSTALLED_APPS = (
    'apps.accounts',
    'apps.common',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
)

WSGI_APPLICATION = 'wsgi.application'

LOCALE_PATHS = []
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'django.request': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

FORCE_SCRIPT_NAME = ""
DEFAULT_TABLESPACE = None
DEFAULT_INDEX_TABLESPACE = None
ABSOLUTE_URL_OVERRIDES = {}
AUTH_USER_MODEL = 'accounts.User'
LANGUAGES_BIDI = []
# MIDDLEWARE_CLASSES = []
DATABASE_ROUTERS = []

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

import django
MEDIA_ROUTE = "uploads"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROUTE)

print django.VERSION