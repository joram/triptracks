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

#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/path/to/django/debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
#
#
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
#
# ROOT_URLCONF = 'urls'
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
#
# BASE_DIR = os.path.normpath(os.path.join(os.path.abspath(__file__), "../../.."))
#
# # MUST OVERRIDE
# DATABASES = {}
#
# ALLOWED_HOSTS = [
#     'triptracks.herokuapp.com',
#     'localhost',
# ]
#
# WSGI_APPLICATION = 'wsgi.application'
#
# LOCALE_PATHS = []
# LOGGING_CONFIG = None
# FORCE_SCRIPT_NAME = ""
# DEFAULT_TABLESPACE = None
# DEFAULT_INDEX_TABLESPACE = None
# ABSOLUTE_URL_OVERRIDES = {}
# AUTH_USER_MODEL = 'accounts.User'
# LANGUAGES_BIDI = []
# DATABASE_ROUTERS = []
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
#
# MEDIA_ROUTE = os.path.join(BASE_DIR, "data/uploads")
# MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROUTE)
