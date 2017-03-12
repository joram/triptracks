# from web.settings.base import *
#
# SECRET_KEY = 'shouldbearealkeyonproduction'
# GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
#
# # postgres://postgres:password@localhost:5432/trip-planner
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'tripplanner',
#         'USER': 'docker',
#         'PASSWORD': 'docker',
#         'HOST': 'localhost',
#         'PORT': 25432,
#     }
# }

from web.settings.prod import *
DEBUG = True
