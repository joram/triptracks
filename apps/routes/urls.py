from django.conf.urls import include, url
from tastypie.api import Api

from api import RouteResource
from views import route

v1_api = Api(api_name='v1')
v1_api.register(RouteResource())


urlpatterns = [
    url(r'^api/routes/all', route.api_all),
    # url(r'^api/', include(v1_api.urls)),
    url(r'^routes/?$', route.list_routes, name='list-routes'),
    url(r'^routes/load/demo/data/', route.tmp_load_data, name='demo-routes'),
    url(r'^routes/upload/', route.upload, name='upload-routes'),
    url(r'^route/create/?$', route.create, name='create-route'),
    url(r'^route/(?P<route_id>[0-9]+)/edit/?$', route.edit, name='edit-route'),
    url(r'^route/(?P<route_id>[0-9]+)/view/?$', route.view, name='view-route'),

]

