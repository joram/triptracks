from django.conf.urls import patterns, include, url

from common.views.home import home
from common.views.plan import create, edit
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trip_planner_www.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', home, name='home'),
    url(r'^plan/create/?$', create, name='create-plan'),
    url(r'^plan/(?P<plan_id>[0-9]+)/edit/?$', edit, name='edit-plan'),
)
