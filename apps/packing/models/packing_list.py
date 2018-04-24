from django.db import models
from utils.fields import ShortUUIDField


class PackingList(models.Model):
    pub_id = ShortUUIDField(prefix="pcklst", max_length=32)
    name = models.CharField(max_length=30, blank=True, default="")

    @property
    def items(self):
        return PackingListItem.objects.filter(packing_list_id=self.id).order_by('-created_at')


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
