from settings.default import *

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = (
  os.path.join(SITE_ROOT, 'static/'),
)

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
)

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
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

SECRET_KEY = os.environ.get("TP_SECRET_KEY", "youshouldntusethisoneinprod")
MEDIA_ROUTE = os.path.join(BASE_DIR, "data/uploads")
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROUTE)

ALLOWED_HOSTS = [
    'app.triptracks.io',
    'triptracks.herokuapp.com',
    'localhost',
]
