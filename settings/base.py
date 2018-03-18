from settings.default import *

# import django
# from django.conf import settings
# settings.configure(DEBUG=True)
# django.setup()

INSTALLED_APPS = (
    'apps.common',
    'apps.accounts',
    'apps.routes',
    'apps.packing',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

)

SECRET_KEY = os.environ.get("TP_SECRET_KEY", "youshouldntusethisoneinprod")
MEDIA_ROUTE = os.path.join(BASE_DIR, "data/uploads")
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROUTE)

ALLOWED_HOSTS = [
    'triptracks.io',
    'triptracks.herokuapp.com',
    'localhost',
]
