from django.conf.urls import url
from views import plan


urlpatterns = [
    url(r'^trip/plan/create/?$', plan.create, name='create-trip-plan'),
    url(r'^trip/plans/?$', plan.list, name='list-trip-plan'),
    url(r'^trip/plan/edit/(?P<pub_id>[0-9a-zA-Z_]+)?$', plan.edit, name='edit-trip-plan'),
    # url(r'^trips/?$', plan.list_plans, name='list-plans'),
]

