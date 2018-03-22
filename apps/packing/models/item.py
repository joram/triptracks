from django.db import models
from jsonfield import JSONField


class Item(models.Model):
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
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'attributes': self.attributes,
            'href': self.href,
            'img_href': self.img_href,
        }
