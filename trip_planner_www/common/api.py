from tastypie import authorization, fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL

from django.contrib.gis.geos import MultiPoint, GEOSGeometry, fromstr
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404

from common.models import Route, Item, PackingList, PackingListItem

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


class ItemResource(ModelResource):
	class Meta:
		queryset = Item.objects.all()
		resource_name = 'item'
		allowed_methods = ('get', 'post', 'put')
		authorization = authorization.Authorization()


class PackingListResource(ModelResource):

	class Meta:
		queryset = PackingList.objects.all()
		resource_name = 'packing_list'
		allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
		authorization = authorization.Authorization()
		fields = ['id', 'name']


class PackingListItemResource(ModelResource):
	item = fields.ForeignKey(ItemResource, 'item')

	class Meta:
		serializer = VerboseSerializer(formats=['json'])
		queryset = PackingListItem.objects.all()
		resource_name = 'packing_list_item'
		allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
		authorization = authorization.Authorization()
		fields = ['id', 'item', 'item_type', 'name', 'quantity']
	
	def dehydrate_item(self, bundle):
		return bundle.obj.item.id
	def hydrate_item(self, bundle):
		print bundle.data
		item = get_object_or_404(Item, id=bundle.data.get('item'))
		bundle.data['item'] = item
		return bundle