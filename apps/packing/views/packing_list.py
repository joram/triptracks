
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.gis.geos import fromstr
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.gdal import DataSource
from django.template.context_processors import csrf
from django.core import serializers
from django.template.loader import render_to_string

import os
import json
# from haystack.query import SearchQuerySet

from apps.packing.forms import PackingListItemForm
from apps.packing.models import Item, PackingList, PackingListItem
from django.http import Http404


def list_packing_lists(request):
    context = {
        'packing_lists': PackingList.objects.all()
    }
    return render_to_response('packing_list/list.html', context)

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

def add_item(request, packing_list_id):
    packing_list = get_object_or_404(PackingList, id=packing_list_id)
    item_name = request.POST.get('search_text')
    qs = Item.objects.filter(description=item_name)
    # qs = SearchQuerySet().filter(description=item_name)
    packing_list_item = None
    if len(qs) == 0:
        raise Http404("no items with search text: %s" % item_name)

    item = qs[0]
    packing_list_item = PackingListItem.objects.create(
        packing_list_id=packing_list_id,
        item_id=item.id,
        name=item_name)

    context = {
        'packing_list_item': packing_list_item
    }
    s = render_to_string('packing_list/_packing_list_item.html', context)
    return JsonResponse({'html': s})


def edit_item(request, packing_list_id, packing_list_item_id):
    form = PackingListItemForm(
        item_id=request.POST.get('item_id'),
        packing_list_id=packing_list_id,
        packing_list_item_id=packing_list_item_id)
    if form.is_valid():
        form.save()

    return JsonResponse({})



def search(request):
    search_text = request.POST.get('search_text')
    quantity = request.POST.get('quantity', 10)
    qs = SearchQuerySet().filter(description=search_text)[:quantity]
    data = {
        'items': [q.object.json for q in qs]
    }
    return JsonResponse(data)
