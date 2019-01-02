import os
import sys


def setup_env():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.dev")
    root_path = os.path.abspath(os.path.split(__file__)[0])
    root_path = os.path.join(root_path, "../..")
    sys.path.insert(0, os.path.join(root_path, 'trip-planner'))
    sys.path.insert(0, root_path)
    import django
    django.setup()
