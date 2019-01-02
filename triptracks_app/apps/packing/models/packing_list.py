from django.db import models
from utils.fields import ShortUUIDField
from apps.packing.models.item import Item


class PackingList(models.Model):
    pub_id = ShortUUIDField(prefix="pcklst", max_length=32)
    name = models.CharField(max_length=30, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def weight(self):
        total_g = sum([item.weight for item in self.items if item.weight is not None])
        if total_g < 1000:
            return "%.2fg" % total_g

        total_kg = total_g/1000
        return "%.2fKg" % total_kg



    @property
    def items(self):
        pl_items = PackingListItem.objects.filter(packing_list_pub_id=self.pub_id)
        return Item.objects.filter(pub_id__in=[pli.item_pub_id for pli in pl_items])

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
