from django.conf.urls import url
from apps.packing.views import item, packing_list


urlpatterns = [
    url(r'^packing/lists/?$', packing_list.list_packing_lists, name='list-packing-lists'),
    url(r'^packing/list/create/?$', packing_list.create, name='create-packing-list'),
    url(r'^packing/list/(?P<pub_id>[0-9a-zA-Z_]+)/edit/?$', packing_list.edit, name='edit-packing-list'),
    url(r'^packing/list/(?P<pub_id>[0-9a-zA-Z_]+)/add/(?P<item_pub_id>[0-9a-zA-Z_]+)/?$', packing_list.add_item, name='add-packing-list-item'),
    url(r'^packing/list/(?P<pub_id>[0-9a-zA-Z_]+)/remove/(?P<item_pub_id>[0-9a-zA-Z_]+)/?$', packing_list.remove_item, name='remove-packing-list-item'),

    url(r'^packing/items/upload/?$', item.upload, name='upload-mec-items'),
    url(r'^packing/items/search/?$', item.search, name='search-items'),
]


