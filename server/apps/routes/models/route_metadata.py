from django.db import models
from utils.fields import ShortUUIDField
from django.contrib.postgres.fields import JSONField


class RouteMetadata(models.Model):
    SOURCE_CHOICES = (
        ("summitpost", 'Summitpost'),
        ("trailpeak", 'Trailpeak'),
    )

    pub_id = ShortUUIDField(prefix="route", max_length=38)
    name = models.CharField(max_length=256)
    geohash = models.CharField(max_length=32)
    bounds = JSONField()
    description = models.TextField(null=True, blank=True)
    source_url = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=16, choices=SOURCE_CHOICES)

    def _get_bounds(self, route):
        min_lat = None
        max_lat = None
        min_lng = None
        max_lng = None
        for line in route.lines:
            for coord in line:
                lat = coord[0]
                lng = coord[1]
                if min_lat is None:
                    min_lat = lat
                    max_lat = lat
                    min_lng = lng
                    max_lng = lng
                min_lat = min(min_lat, lat)
                max_lat = max(max_lat, lat)
                min_lng = min(min_lng, lng)
                max_lng = max(max_lng, lng)
        return (min_lat, min_lng), (max_lat, max_lng)

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
            if len(obj.bounds) == 0:
                obj.bounds = self._get_bounds(obj)
            else:
                print("cached")
            obj.save()

            print(f"{pub_id}\t{created}\t{obj.bounds}")


if __name__ == "__main__":
    RouteMetadata()._load_routes()