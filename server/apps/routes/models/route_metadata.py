from django.db import models
from utils.fields import ShortUUIDField


class RouteMetadata(models.Model):
    pub_id = ShortUUIDField(prefix="route", max_length=38)
    name = models.CharField(max_length=256)
    geohash = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def _load_routes(self):
        from apps.routes.stores.s3_routes import S3RoutesStore
        s = S3RoutesStore()
        manifest = s.get_manifest()
        for pub_id in manifest:
            geohash = manifest.get(pub_id)
            route = s.get_by_pub_id(pub_id)

            print(pub_id, route.name)
            obj, created = RouteMetadata.objects.get_or_create(pub_id=pub_id)
            obj.name = route.name
            obj.description = route.description
            obj.geohash = geohash
            obj.save()

            print(f"{pub_id}\t{created}")
