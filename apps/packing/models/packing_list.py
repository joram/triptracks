from django.db import models
from utils.fields import ShortUUIDField
from apps.packing.models.item import Item


class PackingList(models.Model):
    pub_id = ShortUUIDField(prefix="pcklst", max_length=32)
    name = models.CharField(max_length=30, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def items(self):
        return PackingListItem.objects.filter(packing_list_pub_id=self.pub_id).order_by('-created_at')

    @property
    def item_count(self):
        return self.items.count()


class PackingListItem(models.Model):
    GROUP = "G"
    PERSONAL = "P"
    ITEM_TYPE_CHOICES = ((GROUP, 'Group'), (PERSONAL, 'Personal'))

    item_pub_id = models.CharField(max_length=256)
    packing_list_pub_id = models.CharField(max_length=256)
    item_type = models.CharField(
        max_length=2,
        choices=ITEM_TYPE_CHOICES,
        default=PERSONAL)

    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def item(self):
        return Item.objects.get(pub_id=self.item_pub_id)
