from django.conf.urls import include, url
from tastypie.api import Api

from apps.routes.api import RouteResource
from apps.routes.views import route

v1_api = Api(api_name='v1')
v1_api.register(RouteResource())


urlpatterns = [
    url(r'^api/routes', route.api_all),
    url(r'^api/route/(?P<pub_id>[0-9a-zA-Z_]+)', route.api_route),
    # url(r'^api/', include(v1_api.urls)),
    url(r'^routes/?$', route.browse, name='view-routes'),
    url(r'^routes/mine?$', route.mine, name='view-my-routes'),
    url(r'^routes/load/demo/data/', route.tmp_load_data, name='demo-routes'),
    url(r'^routes/upload/', route.upload, name='upload-routes'),
    url(r'^route/create/?$', route.create, name='create-route'),
    url(r'^route/(?P<route_id>[0-9]+)/edit/?$', route.edit, name='edit-route'),
    url(r'^route/(?P<route_id>[0-9]+)/view/?$', route.view, name='view-route'),

]

