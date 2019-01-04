from django.conf.urls import url
from apps.integrations.views import strava

urlpatterns = [
    url(r'^integrations/strava/connect$', strava.connect),
    url(r'^integrations/strava/authorized$', strava.authorized),
    url(r'^integrations/strava/collect$', strava.collect),
    url(r'^integrations/strava/webhooks$', strava.webhooks),
]
