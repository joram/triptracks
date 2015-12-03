from django.contrib import admin
from common.models import Plan, Map, PackingList, Itinerary

class MapAdmin(admin.ModelAdmin):
    fields = ('plan', 'markers', 'lines')

admin.site.register(Plan)
admin.site.register(Map, MapAdmin)
admin.site.register(PackingList)
admin.site.register(Itinerary)
