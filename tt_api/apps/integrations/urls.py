from django.conf.urls import url
from apps.integrations.views import strava

urlpatterns = [
    url(r'^integrations/strava/webhooks$', strava.webhooks),
]
