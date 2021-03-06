"""trip_planner_www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
import views as route_file_views
from utils.decorators import timed_calls


urlpatterns = [
    url(r'^$', route_file_views.home),
    url(r'^favicon.ico$', route_file_views.favicon),
    url(r'^index.html$', route_file_views.home),
    url(r'^graphql', timed_calls(csrf_exempt(GraphQLView.as_view(graphiql=True)))),
    # url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'', include('apps.routes.urls')),
    url(r'', include('apps.accounts.urls')),
    url(r'', include('apps.packing.urls')),
    url(r'', include('apps.trips.urls')),
    url(r'', include('apps.integrations.urls')),
]


