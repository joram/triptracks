from django.db import models
from django.contrib.auth.models import User
from common.models import PackingList, Itinerary, Route
from jsonfield import JSONField
from common.scrapers.mec import ScrapeMEC
import HTMLParser
parser = HTMLParser.HTMLParser()
import unicodedata


class ItemManager(models.Manager):

	def _parse_price(self, price_str):
		price = price_str.replace("$", "").replace(" ", "")
		if "CAD" in price:
			price = price.split("CAD")[0]
		if "-" in price:
			price = price.split("-")[1]
		price = float(price) if price != '' else -1
		return price

	def load_mec_items(self, quantity=100):
		self.all().delete()

		s = ScrapeMEC()
		added_items = 0
		for data in s.items():
			for k in data.keys():
				try:
					data[k] =  unicodedata.normalize('NFKD', u"%s" % data[k]).encode('utf8', errors='ignore')
				except Exception as e:
					print e

			item, created = self.get_or_create(
				name=data.get('name'),
				price=self._parse_price(data.get('price', '')),
				description=data.get('description'),
				href=data.get('url', ""),
				img_href=data.get('img_href', ""),
				attributes=data)
			added_items += 1
			if added_items > quantity:
				return
			print "%s: %s" % (added_items, item)

class Item(models.Model):
	name = models.CharField(max_length=256)
	description = models.TextField(null=True, blank=True)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	href = models.URLField()
	img_href = models.URLField()

	attributes = JSONField()
	objects = ItemManager()

	def __str__(self):
		return self.name

	@property
	def json(self):
		return {
			'name': self.name,
			'description': self.description,
			'price': self.price,
			'attributes': self.attributes,
			'href': self.href,
			'img_href': self.img_href,
		}

	class Meta:
		app_label = 'common'