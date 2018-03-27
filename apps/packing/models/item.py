from django.db import models
from jsonfield import JSONField
from utils.fields import ShortUUIDField


class Item(models.Model):
    pub_id = ShortUUIDField(prefix="item_", max_length=32)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    href = models.URLField()
    img_href = models.URLField()

    attributes = JSONField()

    def __str__(self):
        return self.name

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
