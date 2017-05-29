from settings.base import *
#
SECRET_KEY = 'shouldbearealkeyonproduction'
GOOGLE_MAPS_API_KEY = os.environ.get("TP_GOOGLE_MAPS_API_KEY")
GOOGLE_CLIENT_ID = os.environ.get("TP_GOOGLE_CLIENT_ID")

DEBUG = True
CSRF_USE_SESSIONS = True

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
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# postgres://postgres:password@localhost:5432/trip-planner
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'tripplanner',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'localhost',
        'PORT': 25432,
    }
}

