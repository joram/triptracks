from django.db import models
# from haystack.query import SearchQuerySet


class PackingList(models.Model):
    name = models.CharField(max_length=30, blank=True, default="")

    @property
    def items(self):
        return PackingListItem.objects.filter(packing_list_id=self.id).order_by('-created_at')


class PackingListItemManager(models.Manager):

    def create(self, *args, **kwargs):
        kwargs['original_name'] = kwargs.get('name')
        return super(PackingListItemManager, self).create(*args, **kwargs)


class PackingListItem(models.Model):
    GROUP = "G"
    PERSONAL = "P"
    ITEM_TYPE_CHOICES = ((GROUP, 'Group'), (PERSONAL, 'Personal'))

    packing_list = models.ForeignKey("PackingList")
    name = models.CharField(max_length=30)
    original_name = models.CharField(max_length=30)
    item_type = models.CharField(
        max_length=2,
        choices=ITEM_TYPE_CHOICES,
        default=PERSONAL)
    item = models.ForeignKey('Item')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PackingListItemManager()

    @property
    def items(self):
        item_image_urls = []
        # for item in SearchQuerySet().filter(description=self.original_name):
        for item in self.objects.filter(description=self.original_name):
            item_image_urls.append((item, self.item.id == item.id))
        return item_image_urls

