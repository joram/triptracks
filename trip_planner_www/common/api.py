from tastypie import authorization
from tastypie.resources import ModelResource
from common.models import Map
from django.core.serializers import serialize
import pdb
from django.contrib.gis.geos import MultiPoint, GEOSGeometry, fromstr
import json


class MapResource(ModelResource):
	class Meta:
	    queryset = Map.objects.all()
	    resource_name = 'map'
	    allowed_methods = ('get')
	    exclude = ['plan']
	    authorization = authorization.Authorization()