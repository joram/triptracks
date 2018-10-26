from django.conf.urls import url
from apps.integrations.views import strava
from apps.integrations.strava_worker import *  # to trigger the collection thread

urlpatterns = [
    url(r'^integrations/strava/connect$', strava.connect),
    url(r'^integrations/strava/authorized$', strava.authorized),
    url(r'^integrations/strava/collect$', strava.collect),
]
