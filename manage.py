#!/usr/bin/env python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

from django.contrib.gis.geos import libgeos

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
