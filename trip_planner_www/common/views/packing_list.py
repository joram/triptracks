
from django.conf import settings
from django.shortcuts import get_object_or_404
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

from common.models import Item, PackingList


def create(request):
	packing_list = PackingList.objects.create(name="Unnamed List")
	return redirect('edit-packing-list', packing_list.id)

def edit(request, packing_list_id):
	packing_list = get_object_or_404(PackingList, id=packing_list_id)
	context = {
		'packing_list': packing_list
	}
	context.update(csrf(request))
	return render_to_response('packing_list/edit.html', context)


def search(request):
	search_text = request.POST.get('search_text')
	quantity = request.POST.get('quantity', 10)
	print "searching for: %s" % search_text
	qs = SearchQuerySet().filter(description=search_text)[:quantity]
	data = {
		'items': [q.object.json for q in qs]
	}
	return JsonResponse(data)
