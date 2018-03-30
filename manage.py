#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    import django
    django.setup()

    from django.core.management.commands.runserver import Command as runserver
    port = os.environ.get("PORT", "8000")
    print "running on port {}".format(port)
    runserver.default_port = port

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
