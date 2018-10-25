#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    import django
    django.setup()

    from apps.integrations.strava_worker import start as collect_strava_data
    collect_strava_data()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
