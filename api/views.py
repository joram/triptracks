from django.http import HttpResponse
from django.views.generic.base import RedirectView

favicon = RedirectView.as_view(url='/static/favicon.ico', permanent=True)


def home(request):
    return HttpResponse("hello, this is an API, you should go to <a href='https://www.triptracks.io'>www.triptracks.io</a>, it's for humans.")

