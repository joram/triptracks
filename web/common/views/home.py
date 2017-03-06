from django.conf import settings
from django.shortcuts import render_to_response


def home(request):
    context = {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    }
    return render_to_response("home.html", context)