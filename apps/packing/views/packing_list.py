from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
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
    pl_items = PackingListItem.objects.filter(packing_list_pub_id=pub_id)
    items = Item.objects.filter(pub_id__in=[pli.item_pub_id for pli in pl_items]).order_by('created_at')

    context = {
        'packing_list': packing_list,
        'items': items
    }
    context.update(csrf(request))
    return render_to_response('packing/edit.html', context)


@login_required
def add_item(request, pub_id, item_pub_id):
    packing_list = get_object_or_404(PackingList, pub_id=pub_id)
    item = get_object_or_404(Item, pub_id=item_pub_id)
    PackingListItem.objects.create(
        packing_list_pub_id=pub_id,
        item_pub_id=item_pub_id,
    )
    return HttpResponse()


@login_required
def remove_item(request, pub_id, item_pub_id):
    packing_list = get_object_or_404(PackingList, pub_id=pub_id)
    item = get_object_or_404(Item, pub_id=item_pub_id)
    PackingListItem.objects.filter(
        packing_list_id=packing_list.id,
        item_id=item.id,
        name=item.name
    ).delete()
    return HttpResponse()


@login_required
def edit_item(request, packing_list_id, packing_list_item_id):
    form = PackingListItemForm(
        item_id=request.POST.get('item_id'),
        packing_list_id=packing_list_id,
        packing_list_item_id=packing_list_item_id)
    if form.is_valid():
        form.save()

    return JsonResponse({})
