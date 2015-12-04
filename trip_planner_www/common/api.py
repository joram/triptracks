from tastypie import authorization
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL

from django.contrib.gis.geos import MultiPoint, GEOSGeometry, fromstr
from django.core.serializers import serialize

from common.models import Route


class RouteResource(ModelResource):
	class Meta:
		queryset = Route.objects.all()
		resource_name = 'route'
		allowed_methods = ('get', 'post', 'put')
		authorization = authorization.Authorization()
		exclude = ['plan']

		filtering = {
			'markers': ALL,
			'lines': ALL,
		}