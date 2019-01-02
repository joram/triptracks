from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect

from apps.packing.models import Item, PackingList, PackingListItem
from apps.common.decorators import login_required


@login_required
def list_packing_lists(request):
    context = {
        'packing_lists': PackingList.objects.all().order_by('updated_at')
    }
    return render(request, 'packing/list.html', context)


@login_required
def create(request):
    packing_list = PackingList.objects.create(name="Unnamed List")
    return redirect('edit-packing-list', packing_list.pub_id)


@login_required
def edit(request, pub_id):
    packing_list = get_object_or_404(PackingList, pub_id=pub_id)

    if request.method == "POST":
        name = request.POST.get("name")
        packing_list.name = name
        packing_list.save()
        return HttpResponse()

    pl_items = PackingListItem.objects.filter(packing_list_pub_id=pub_id)
    items = Item.objects.filter(pub_id__in=[pli.item_pub_id for pli in pl_items])

    context = {
        'packing_list': packing_list,
        'items': items
    }
    return render(request, 'packing/edit.html', context)


@login_required
def add_item(request, pub_id, item_pub_id):
    get_object_or_404(PackingList, pub_id=pub_id)
    get_object_or_404(Item, pub_id=item_pub_id)
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
