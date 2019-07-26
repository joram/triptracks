from django.conf.urls import url
from apps.accounts.views import auth as auth_views


def debug(request):
    import os
    from django.http import HttpResponse
    got = len(os.environ.get("TT_DATABASE_URL")) > 0
    return HttpResponse(str(got))


urlpatterns = [
    url(r'^debug$', debug),
    url(r'^login$', auth_views.login),
    url(r'^logout$', auth_views.logout),
]
