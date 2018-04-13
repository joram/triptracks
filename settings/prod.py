from settings.base import *
import dj_database_url
import os

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
# GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')

SECRET_KEY = os.environ.get("TP_SECRET_KEY", "youshouldntusethisoneinprod")
GOOGLE_MAPS_API_KEY = os.environ.get("TP_GOOGLE_MAPS_API_KEY")
GOOGLE_CLIENT_ID = os.environ.get("TP_GOOGLE_CLIENT_ID")
CSRF_USE_SESSIONS = True


DATABASES = {'default': dj_database_url.config(env="TP_DATABASE_URL")}
DATABASES["default"]["NAME"] = DATABASES["default"]["NAME"].rstrip("\r")
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}


DEBUG = False

