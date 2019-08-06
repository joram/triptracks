from settings.default import *
import os
import newrelic.agent
# newrelic.agent.initialize('newrelic.ini')

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = (
  os.path.join(SITE_ROOT, 'static/'),
)

STAFF_EMAILS = os.getenv("TT_STAFF_EMAILS", "").rstrip("\r").split(",")

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'graphene_django',
    'apps.accounts',
    'apps.routes',
    'apps.packing',
    'apps.trips',
    'apps.integrations',
    'corsheaders',
)

GRAPHENE = {'SCHEMA': 'schema.schema'}

LOGGING_CONFIG = 'logging.config.dictConfig'
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'django.request': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

SECRET_KEY = os.environ.get("TT_SECRET_KEY", "youshouldntusethisoneinprod")
MEDIA_ROUTE = os.path.join(BASE_DIR, "data/uploads")
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROUTE)

import re
from django.template import base
base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)

ALLOWED_HOSTS = [
    'www.triptracks.io',
    'localhost',
]
