from django.contrib import admin
from apps.packing.models import Plan, PackingList, PackingListItem, Itinerary, Item


admin.site.register(Plan)
admin.site.register(PackingList)
admin.site.register(PackingListItem)
admin.site.register(Itinerary)
admin.site.register(Item)
