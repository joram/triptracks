web: python ./manage.py runserver 0.0.0.0:$PORT --settings=settings.prod
web_fdsaf: gunicorn wsgi  --env DJANGO_SETTINGS_MODULE=settings.prod
