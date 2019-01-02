#!/usr/bin/env python
import os
import json
from flask import render_template, Flask, request, send_from_directory
import geohash2
from stores.cached_routes import CachedRoutesStore
from stores.routes import RoutesStore
app = Flask(__name__)
app.debug = True
base_store = RoutesStore()
stores = {
  0: CachedRoutesStore(1, base_store),
  1: CachedRoutesStore(1, base_store),
  2: CachedRoutesStore(1, base_store),
  3: CachedRoutesStore(5, base_store),
  4: CachedRoutesStore(5, base_store),
  5: CachedRoutesStore(5, base_store),
  6: CachedRoutesStore(10, base_store),
  7: CachedRoutesStore(10, base_store),
  8: CachedRoutesStore(10, base_store),
  9: CachedRoutesStore(25, base_store),
  10: CachedRoutesStore(25, base_store),
  11: CachedRoutesStore(100, base_store),
  12: CachedRoutesStore(100, base_store),
  13: CachedRoutesStore(500, base_store),
  14: CachedRoutesStore(500, base_store),
  15: CachedRoutesStore(1000, base_store),
  16: CachedRoutesStore(1000, base_store),
  17: CachedRoutesStore(1500, base_store),
  18: CachedRoutesStore(1500, base_store),
  19: CachedRoutesStore(2000, base_store),
  20: CachedRoutesStore(2000, base_store),
}


@app.route('/favicon.ico')
def favicon():
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


def geohash(bbox):
  ((lat1, lng1), (lat2, lng2)) = bbox
  h1 = geohash2.encode(lat1, lng1)
  h2 = geohash2.encode(lat2, lng2)
  i = 0
  for c in h1:
    if h2[i] == c:
      i += 1
  matching = h1[:i]
  return matching


@app.route('/')
def hello():
  return render_template('home.html')


@app.route('/routes')
def routes():
  # bbox_coords = (xmin, ymin, xmax, ymax)
  # "lat_lo,lng_lo,lat_hi,lng_hi"
  bbox = request.args.get('bbox').split(",")
  zoom = int(request.args.get('zoom'))
  bbox = [float(val) for val in bbox]
  bbox = ((bbox[0], bbox[1]), (bbox[2], bbox[3]))
  g = geohash(bbox)
  routes, cache_hit = stores[zoom].get(g)
  print("bbox={} geohash={} zoom={} num_routes={} cache_hit={}".format(bbox, g, zoom, len(routes), cache_hit))

  data = {}
  for r in routes:
      data[r["pub_id"]] = {"name": r["name"], "lines":r["lines"]}
  return json.dumps({
    "routes": data,
    "geohash": g,
    "zoom": zoom,
  #  "max_vertices": store.MAX_VERTICES.get(zoom),
  }, sort_keys=True, indent=2, separators=(',', ': '))


if __name__ == '__main__':
  app.run()
# routes.append({
#   'center': center,
#   'name': route["name"],
#   'description': route["description"],
#   'image_url': route["image_url"],
#   'pub_id': route["pub_id"],
#   'zoom_level': zoom_level,
#   'lines': json.loads(route[zoom_field_name]),
#   'is_mine': route["owner_pub_id"] == user_pub_id,
#   'is_public': route["is_public"],
# })

