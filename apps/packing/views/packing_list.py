from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.template.loader import render_to_string

from apps.packing.forms import PackingListItemForm
from apps.packing.models import Item, PackingList, PackingListItem
from apps.common.decorators import login_required


@login_required
def list_packing_lists(request):
    context = {
        'packing_lists': PackingList.objects.all()
    }
    return render_to_response('packing/list.html', context)


@login_required
def create(request):
    packing_list = PackingList.objects.create(name="Unnamed List")
    return redirect('edit-packing-list', packing_list.pub_id)


@login_required
def edit(request, pub_id):
    packing_list = get_object_or_404(PackingList, pub_id=pub_id)
    context = {
        'packing_list': packing_list
    }
    context.update(csrf(request))
    return render_to_response('packing/edit.html', context)


@login_required
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
    s = render_to_string('packing/_packing_list_item.html', context)
    return JsonResponse({'html': s})


@login_required
def edit_item(request, packing_list_id, packing_list_item_id):
    form = PackingListItemForm(
        item_id=request.POST.get('item_id'),
        packing_list_id=packing_list_id,
        packing_list_item_id=packing_list_item_id)
    if form.is_valid():
        form.save()

    return JsonResponse({})
