import json
from scrapers.trailpeak_details import ScrapeTrailPeakDetails
from apps.routes.models import Route, lines_from_gpx
from apps.routes.stores import S3RoutesStore


# store = RoutesStore()
store = S3RoutesStore()
if __name__ == "__main__":
  s = ScrapeTrailPeakDetails()
  for data in s.run():
    if "note" in data:
        continue
    data = json.loads(data)
    route = Route.from_data(data)
    p = data["gpx_filepath"].replace("/mnt/c/Users/john/triptracks", ".")
    route.lines = lines_from_gpx(p)
    num_verts = sum(len(l) for l in route.lines)
    if num_verts > 0:
      store.add(route)

