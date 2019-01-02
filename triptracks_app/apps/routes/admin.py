from django.contrib import admin
from apps.routes.models import Route, TracksFile


class RouteAdmin(admin.ModelAdmin):
    fields = ('markers', 'lines', 'center')

admin.site.register(Route, RouteAdmin)
admin.site.register(TracksFile)
