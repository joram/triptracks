#!/usr/bin/env python
import sys

if __name__ == "__main__":
    import django
    django.setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
