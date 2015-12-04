from django.conf.urls import patterns, include, url
from tastypie.api import Api
from django.contrib import admin

from common.api import RouteResource
from common.views.home import home
from common.views.plan import create, edit

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(RouteResource())


urlpatterns = patterns('',
    url(r'^/?$', home, name='home'),
    url(r'^plan/create/?$', create, name='create-plan'),
    url(r'^plan/(?P<plan_id>[0-9]+)/edit/?$', edit, name='edit-plan'),
	
	url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
