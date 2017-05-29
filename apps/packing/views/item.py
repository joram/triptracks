import os
import json

from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.gdal import DataSource

from apps.packing.models import Item


def upload(request):
	Item.objects.load_mec_items()
	return redirect('list-routes')