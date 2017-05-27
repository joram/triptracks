from django.conf import settings
from django.shortcuts import render_to_response
from geoip import geolite2


def get_client_lat_long(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print ip
    match = geolite2.lookup('17.0.0.1')
    return match.location


def home(request):
    context = {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
    }
    return render_to_response("home.html", context)
