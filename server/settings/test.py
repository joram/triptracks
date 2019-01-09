from settings.base import *
import dj_database_url
import os

BASE_URL = "https://app.triptracks.io"

SECRET_KEY = os.environ.get("TT_SECRET_KEY", "youshouldntusethisoneinprod")
GOOGLE_MAPS_API_KEY = os.environ.get("TT_GOOGLE_MAPS_API_KEY")
GOOGLE_CLIENT_ID = os.environ.get("TT_GOOGLE_CLIENT_ID")
CSRF_USE_SESSIONS = True

STRAVA_CLIENT_ID = os.environ.get("TT_STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get("TT_STRAVA_CLIENT_SECRET")
STRAVA_ACCESS_TOKEN = os.environ.get("TT_STRAVA_ACCESS_TOKEN")
STRAVA_REFRESH_TOKEN = os.environ.get("TT_STRAVA_REFRESH_TOKEN")
STRAVA_VERIFY_TOKEN = os.environ.get("TT_STRAVA_VERIFY_TOKEN")

DEBUG = False

