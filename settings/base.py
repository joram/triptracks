from settings.default import *
import os

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
    'django.contrib.gis',

    'apps.common',
    'apps.accounts',
    'apps.routes',
    'apps.packing',
    'apps.trips',
    'apps.integrations',
)

from django.contrib.gis import *
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
            'class':'logging.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': False,
            'level':'DEBUG',
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
# from django.template.context_processors import request
# TEMPLATES[0]["OPTIONS"]["context_processors"] += ""

ALLOWED_HOSTS = [
    'app.triptracks.io',
    'triptracks.herokuapp.com',
    'localhost',
    '199.245.58.143',
]
