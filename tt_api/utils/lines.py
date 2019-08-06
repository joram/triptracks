import gpxpy.gpx
import geohash2
import geopy.distance


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


def bbox(lines):
  min_lat = None
  max_lat = None
  min_lng = None
  max_lng = None
  for line in lines:
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


def lines_from_gpx_string(content):
  try:
    gpx = gpxpy.parse(content)
  except:
    return []
  return _lines_from_gpx(gpx)


def lines_from_gpx(filepath):
  if filepath.endswith(".json"):
    filepath = filepath.replace(".json", ".gpx")
  with open(filepath) as f:
    gpx = gpxpy.parse(f)
  return _lines_from_gpx(gpx)


def _lines_from_gpx(gpx):
  lines = []
  for track in gpx.tracks:
    for segment in track.segments:
      line = []
      for point in segment.points:
        line.append((point.latitude, point.longitude, point.elevation))
      if len(line) > 0:
        lines.append(line)

  for route in gpx.routes:
    line = []
    for point in route.points:
      line.append((point.latitude, point.longitude, point.elevation))
    if len(line) > 0:
        lines.append(line)

  # fallback to waypoints
  if len(lines) == 0:
    for point in gpx.waypoints:
      line = [(point.latitude, point.longitude, point.elevation)]
      lines.append(line)

  return lines


def _max_verts(line, zoom):
  verts_per_km = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 1,
    10: 5,
    11: 5,
    12: 5,
    13: 10,
    14: 10,
    15: 20,
    16: 20,
    17: 50,
    18: 50,
    19: 100,
    20: 100,
  }[zoom]
  d = km(line)
  x = max(1, int(verts_per_km * d))
  return x


def reduced_lines(lines, zoom):
  new_lines = []
  for line in lines:
    new_lines.append(reduced_line(line, _max_verts(line, zoom)))
  return new_lines


def km(line):
  length = 0
  for i in range(0, (len(line)-1)):
    try:
      length += geopy.distance.vincenty(line[i], line[i+1]).km
    except:
      pass
  return length


def reduced_line(line, max_vertices):
  if max_vertices == 0:
    max_vertices = 1

  if len(line) < max_vertices:
    return line

  step = int(len(line) / max_vertices)
  new_line = [line[0]]
  i = 0
  for i in range(0, len(line) - 1, step):
    new_line.append(line[i])
  if i != len(line):
    new_line.append(line[-1])
  return new_line
