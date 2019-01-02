from django.conf import settings
from django.shortcuts import render_to_response
from django.middleware.csrf import get_token


def home(request):
    context = {
        'request': request,
        "csrf_token": get_token(request),
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    }
    return render_to_response("home.html", context)
