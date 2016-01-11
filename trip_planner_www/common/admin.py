from django.contrib import admin
from common.models import Plan, Route, PackingList, PackingListItem, Itinerary, Item, TracksFile

class RouteAdmin(admin.ModelAdmin):
    fields = ('markers', 'lines', 'center')

admin.site.register(Plan)
admin.site.register(Route, RouteAdmin)
admin.site.register(PackingList)
admin.site.register(PackingListItem)
admin.site.register(Itinerary)
admin.site.register(Item)
admin.site.register(TracksFile)
