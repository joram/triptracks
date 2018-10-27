from settings.base import *
import os
import dj_database_url

BASE_URL = "http://localhost:8000"
SECRET_KEY = os.environ.get("TT_SECRET_KEY", "youshouldntusethisoneinprod")
GOOGLE_MAPS_API_KEY = os.environ.get("TT_GOOGLE_MAPS_API_KEY")
GOOGLE_CLIENT_ID = os.environ.get("TT_GOOGLE_CLIENT_ID")

STRAVA_CLIENT_ID = os.environ.get("TT_STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get("TT_STRAVA_CLIENT_SECRET")
STRAVA_ACCESS_TOKEN = os.environ.get("TT_STRAVA_ACCESS_TOKEN")
STRAVA_REFRESH_TOKEN = os.environ.get("TT_STRAVA_REFRESH_TOKEN")
STRAVA_VERIFY_TOKEN = os.environ.get("TT_STRAVA_VERIFY_TOKEN")

DATABASES = {'default': dj_database_url.config(env="TT_DATABASE_URL")}
DATABASES["default"]["NAME"] = DATABASES["default"]["NAME"].rstrip("\r")
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
DEBUG = True



