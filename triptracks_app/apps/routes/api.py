from tastypie import authorization, fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL

from apps.routes.models import Route

import json
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest


class VerboseSerializer(Serializer):
	"""
	Gives message when loading JSON fails.
	"""
	# Tastypie>=0.9.6,<=0.11.0
	def from_json(self, content):
		"""
		Override method of `Serializer.from_json`. Adds exception message when loading JSON fails.
		"""
		try:
			return json.loads(content)
		except ValueError as e:
			raise BadRequest(u"Incorrect JSON format: Reason: \"{}\" (See www.json.org for more info.)".format(e.message))


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

