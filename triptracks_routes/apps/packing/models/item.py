from django.db import models
from jsonfield import JSONField
from utils.fields import ShortUUIDField
# from scrapers.mec_raw_html import ScrapeMEC
import json


class ItemManager(models.Manager):

    def _parse_price(self, price_str):
        try:
            for bad in ["$", " ", "Available", "prices"]:
                price_str = price_str.replace(bad, "")
            price = float(price_str) if price_str != '' else -1
            return price
        except:
            return -2

    # def collect_and_load_all(self):
    #     scraper = ScrapeMEC()
    #     for id, filepath, data in scraper.items():
    #         data = json.loads(data)
    #         qs = self.filter(name=data.get("title"))
    #         if qs.exists():
    #             print(u"EXISTS: {}".format(data.get("title")))
    #             continue
    #
    #         self.get_or_create(
    #             name=data.get('title'),
    #             price=self._parse_price(data.get('price', '')),
    #             description=data.get('description'),
    #             href=data.get('url', ""),
    #             img_href=data.get('img_href', ""),
    #             attributes=data)
    #         print(u"CREATED: {}".format(data.get("title")))


class Item(models.Model):
    pub_id = ShortUUIDField(prefix="item", max_length=32)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    href = models.URLField()
    img_href = models.URLField()
    attributes = JSONField()

    _weight = None

    objects = ItemManager()

    def __str__(self):
        return self.name

    @property
    def weight(self):

        def grams(s):
            s = s.lower()
            if s.endswith("kg"):
                v = s.replace("kg", "")
                v = float(v)
                return v*1000

            if s.endswith("g"):
                v = s.replace("g", "")
                v = float(v)
                return v

        if self._weight is None:
            for key in self.attributes.keys():
                if key.lower() == "weight":
                    self._weight = grams(self.attributes[key])
                    break

        return self._weight

    @property
    def json(self):
        return {
            'pub_id': self.pub_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'attributes': self.attributes,
            'href': self.href,
            'img_href': self.img_href,
        }
