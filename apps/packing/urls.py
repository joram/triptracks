from django.conf.urls import include, url
from tastypie.api import Api
from api import ItemResource, PackingListResource, PackingListItemResource
from views import item, packing_list

v1_api = Api(api_name='v1')
v1_api.register(ItemResource())
v1_api.register(PackingListResource())
v1_api.register(PackingListItemResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    url(r'^items/upload/?$', item.upload, name='upload-mec-items'),
    url(r'^lists/?$', packing_list.list_packing_lists, name='list-packing-lists'),
	url(r'^list/create/?$', packing_list.create, name='create-packing-list'),
    url(r'^list/(?P<packing_list_id>[0-9]+)/edit/?$', packing_list.edit, name='edit-packing-list'),
    url(r'^list/(?P<packing_list_id>[0-9]+)/item/add/?$', packing_list.add_item, name='add-packing-list-item'),
    url(r'^list/(?P<packing_list_id>[0-9]+)/item/(?P<packing_list_item_id>[0-9]+)/edit/?$', packing_list.edit_item, name='edit-packing-list-item'),
    url(r'^list/items/search/?$', packing_list.search, name='search-packing-list'),
]

