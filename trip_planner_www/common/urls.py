from django.conf.urls import patterns, include, url
from tastypie.api import Api
from django.contrib import admin

from common.api import RouteResource, ItemResource
from common.views.home import home
from common.views import route, item, packing_list


v1_api = Api(api_name='v1')
v1_api.register(RouteResource())
v1_api.register(ItemResource())


urlpatterns = patterns('',
    url(r'^/?$', home, name='home'),	
    url(r'^api/', include(v1_api.urls)),

    url(r'^routes/?$', route.list_routes, name='list-routes'),
    url(r'^routes/load/demo/data/', route.tmp_load_data, name='demo-routes'),
    url(r'^routes/upload/', route.upload, name='upload-routes'),
    url(r'^route/create/?$', route.create, name='create-route'),
    url(r'^route/(?P<route_id>[0-9]+)/edit/?$', route.edit, name='edit-route'),
    url(r'^route/(?P<route_id>[0-9]+)/view/?$', route.view, name='view-route'),

    url(r'^items/upload/?$', item.upload, name='upload-mec-items'),
	
	url(r'^packing/lists/create/?$', packing_list.create, name='create-packing-list'),
    url(r'^packing/lists/items/search/?$', packing_list.search, name='search-packing-list'),
)

