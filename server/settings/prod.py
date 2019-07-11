from settings.base import *
import dj_database_url
import os

BASE_URL = "https://app.triptracks.io"

SECRET_KEY = os.environ.get(u"TT_SECRET_KEY", "youshouldntusethisoneinprod")
GOOGLE_MAPS_API_KEY = os.environ.get(u"TT_GOOGLE_MAPS_API_KEY")
GOOGLE_CLIENT_ID = os.environ.get(u"TT_GOOGLE_CLIENT_ID")
CSRF_USE_SESSIONS = True

STRAVA_CLIENT_ID = os.environ.get(u"TT_STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get(u"TT_STRAVA_CLIENT_SECRET")
STRAVA_ACCESS_TOKEN = os.environ.get(u"TT_STRAVA_ACCESS_TOKEN")
STRAVA_REFRESH_TOKEN = os.environ.get(u"TT_STRAVA_REFRESH_TOKEN")
STRAVA_VERIFY_TOKEN = os.environ.get(u"TT_STRAVA_VERIFY_TOKEN")


# DATABASES = {'default': dj_database_url.config()}
DATABASES = {'default': dj_database_url.config(env=u"TT_DATABASE_URL")}

DEBUG = False
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    BASE_URL,
)