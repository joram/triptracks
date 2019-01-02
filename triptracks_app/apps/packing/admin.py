from django.contrib import admin
from apps.packing.models import PackingList, PackingListItem, Item


admin.site.register(PackingList)
admin.site.register(PackingListItem)
admin.site.register(Item)
