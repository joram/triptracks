from django.conf.urls import patterns, include, url
from tastypie.api import Api
from django.contrib import admin

from common.api import RouteResource
from common.views.home import home
from common.views import route

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(RouteResource())


urlpatterns = patterns('',
    url(r'^/?$', home, name='home'),
    url(r'^routes/?$', route.list_routes, name='list-routes'),
    url(r'^route/create/?$', route.create, name='create-route'),
    url(r'^route/(?P<route_id>[0-9]+)/edit/?$', route.edit, name='edit-route'),
    url(r'^route/(?P<route_id>[0-9]+)/view/?$', route.view, name='view-route'),
    url(r'^routes/load/demo/data/', route.tmp_load_data, name='demo-routes'),
	
	url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    (r'^search/', include('haystack.urls')),
)
