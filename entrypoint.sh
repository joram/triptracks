#!/bin/bash

django-admin.py makemigrations
django-admin.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | django-admin.py shell
django-admin.py load_mec_data 5000
django-admin.py load_demo_tracks

yes y | django-admin.py rebuild_index
django-admin.py runserver 0.0.0.0:8000