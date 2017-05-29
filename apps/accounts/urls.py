from django.conf.urls import url
from apps.accounts.views.login import google_login_token

urlpatterns = [
    url(r'^google_account_logged_in$', google_login_token),
]
