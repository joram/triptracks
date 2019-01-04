import json
from scrapers.trailpeak_details import ScrapeTrailPeakDetails
from models.route import Route, lines_from_gpx
from stores.routes import RoutesStore


store = RoutesStore()
if __name__ == "__main__":
  s = ScrapeTrailPeakDetails()
  for data in s.run():
    if "note" in data:
        continue
    data = json.loads(data)
    route = Route.from_data(data)
    route.lines = lines_from_gpx(data["gpx_filepath"])
    num_verts = sum(len(l) for l in route.lines)
    print(route.pub_id, num_verts, route.name)
    store.add(route)

