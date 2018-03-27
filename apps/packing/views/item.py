from django.shortcuts import redirect
from django.http import JsonResponse
from apps.packing.models import Item


def upload(request):
    Item.objects.load_mec_items()
    return redirect('list-routes')


def search(request):
    search_text = request.GET.get('text', "")
    quantity = max(10, request.GET.get('quantity', 10))
    if search_text == "":
        qs = []
    else:
        qs = Item.objects.filter(name__icontains=search_text)[:quantity]
    data = {
        'count': len(qs),
        'items': [item.json for item in qs]
    }
    return JsonResponse(data)
