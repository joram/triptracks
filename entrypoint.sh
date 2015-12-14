#!/bin/bash
# django-admin.py migrate

# if [ ! -d /srv ]; then mkdir /srv fi;
# if [ ! -d /srv/logs ]; then mkdir /srv/logs fi;

# # Prepare log files and start outputting logs to stdout
# touch /srv/logs/gunicorn.log
# touch /srv/logs/access.log
# tail -n 0 -f /srv/logs/*.log &

# ls -hal
# env

# # Start Gunicorn processes
# echo Starting Gunicorn.
# exec gunicorn trip-planner.wsgi:application \
#     --name hello_django \
#     --bind 0.0.0.0:8000 \
#     --workers 3 \
#     --log-level=info \
#     --log-file=/srv/logs/gunicorn.log \
#     --access-logfile=/srv/logs/access.log \
#     "$@"

django-admin.py makemigrations
django-admin.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | django-admin.py shell
django-admin.py runserver 0.0.0.0:8000