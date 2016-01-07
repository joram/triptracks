
from django.conf import settings
from django.contrib.gis.geos import fromstr
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.gdal import DataSource
from django.template.context_processors import csrf
from django.core import serializers

import os
import json
from haystack.query import SearchQuerySet

from common.models import Item


def create(request):
	context = {}
	context.update(csrf(request))
	return render_to_response('create_packing_list/index.html', context)


def search(request):
	search_text = request.POST.get('search_text')
	print "searching for: %s" % search_text
	qs = SearchQuerySet().filter(description=search_text)
	data = {
		'items': [q.object.json for q in qs]
	}
	return JsonResponse(data)
