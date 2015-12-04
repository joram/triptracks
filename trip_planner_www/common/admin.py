from django.contrib import admin
from common.models import Plan, Route, PackingList, Itinerary

class RouteAdmin(admin.ModelAdmin):
    fields = ('markers', 'lines')

admin.site.register(Plan)
admin.site.register(Route, RouteAdmin)
admin.site.register(PackingList)
admin.site.register(Itinerary)
