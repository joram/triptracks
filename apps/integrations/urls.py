from django.conf.urls import url
from apps.integrations.views import strava

urlpatterns = [
    url(r'^integrations/strava/connect$', strava.connect),
    url(r'^integrations/strava/authorized$', strava.authorized),
]
