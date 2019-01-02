from django.views.generic.base import RedirectView
from django.conf.urls import url
from apps.common.views.home import home

favicon_view = RedirectView.as_view(url='/static/img/favicon.png', permanent=True)

urlpatterns = [
    url(r'^favicon.ico', favicon_view),
    url(r'^$', home, name='home'),
]