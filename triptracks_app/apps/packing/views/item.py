from django.shortcuts import redirect
from django.http import JsonResponse
from apps.packing.models import Item
from apps.common.decorators import login_required


@login_required
def upload(request):
    Item.objects.load_mec_items()
    return redirect('list-routes')


@login_required
def search(request):
    search_text = request.GET.get('text', "")
    quantity = min(10, int(request.GET.get('quantity', '10')))
    query_funcs = [
        exact_match_name,
        exact_match_description,
        one_word_match_name,
        one_word_match_description,
    ]

    data = {
        'count': 0,
        'items': []
    }

    for func in query_funcs:
        remaining = quantity - data['count']
        if remaining <= 0:
            break
        items = func(search_text, remaining)
        data["items"] += [item.json for item in items]
        data["count"] += len(items)

    return JsonResponse(data)


def exact_match_name(search_text, quantity):
    return list(Item.objects.filter(name__icontains=search_text)[:quantity])


def one_word_match_name(search_text, quantity):
    search_words = [w for w in search_text.split(" ") if w != ""]
    items = []
    for word in search_words:
        qs = Item.objects.filter(name__icontains=word)[:quantity-len(items)]
        items += list(qs)
    return items


def exact_match_description(search_text, quantity):
    return list(Item.objects.filter(description__icontains=search_text)[:quantity])


def one_word_match_description(search_text, quantity):
    search_words = [w for w in search_text.split(" ") if w != ""]
    items = []
    for word in search_words:
        qs = Item.objects.filter(description__icontains=word)[:quantity-len(items)]
        items += list(qs)
    return items
