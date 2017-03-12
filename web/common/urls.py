from django.conf.urls import include, url
from tastypie.api import Api

from api import RouteResource, ItemResource, PackingListResource, PackingListItemResource
from views.home import home
from views import route, item, packing_list
from django.views.generic.base import RedirectView


v1_api = Api(api_name='v1')
v1_api.register(RouteResource())
v1_api.register(ItemResource())
v1_api.register(PackingListResource())
v1_api.register(PackingListItemResource())


favicon_view = RedirectView.as_view(url='/static/img/favicon.png', permanent=True)

urlpatterns = [

    url(r'^/?$', home, name='home'),
    url(r'^favicon.ico', favicon_view),

    url(r'^api/', include(v1_api.urls)),
    url(r'^routes/?$', route.list_routes, name='list-routes'),
    url(r'^routes/load/demo/data/', route.tmp_load_data, name='demo-routes'),
    url(r'^routes/upload/', route.upload, name='upload-routes'),
    url(r'^route/create/?$', route.create, name='create-route'),
    url(r'^route/(?P<route_id>[0-9]+)/edit/?$', route.edit, name='edit-route'),
    url(r'^route/(?P<route_id>[0-9]+)/view/?$', route.view, name='view-route'),

    url(r'^items/upload/?$', item.upload, name='upload-mec-items'),

    url(r'^lists/?$', packing_list.list_packing_lists, name='list-packing-lists'),
	url(r'^list/create/?$', packing_list.create, name='create-packing-list'),
    url(r'^list/(?P<packing_list_id>[0-9]+)/edit/?$', packing_list.edit, name='edit-packing-list'),
    url(r'^list/(?P<packing_list_id>[0-9]+)/item/add/?$', packing_list.add_item, name='add-packing-list-item'),
    url(r'^list/(?P<packing_list_id>[0-9]+)/item/(?P<packing_list_item_id>[0-9]+)/edit/?$', packing_list.edit_item, name='edit-packing-list-item'),
    url(r'^list/items/search/?$', packing_list.search, name='search-packing-list'),
]

