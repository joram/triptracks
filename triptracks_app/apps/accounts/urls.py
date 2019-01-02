from django.conf.urls import url
from apps.accounts.views import auth as auth_views

urlpatterns = [
    url(r'^login$', auth_views.login),
    url(r'^logout$', auth_views.logout),
]
