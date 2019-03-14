import gpxpy.gpx
import geohash2


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
  gpx = gpxpy.parse(content)
  return _lines_from_gpx(gpx)


def lines_from_gpx(filepath):
  try:
    if filepath.endswith(".json"):
      filepath = filepath.replace(".json", ".gpx")
    with open(filepath) as f:
      gpx = gpxpy.parse(f)
  except Exception as e:
    return []
  return _lines_from_gpx(gpx)


def _lines_from_gpx(gpx):
  lines = []
  for track in gpx.tracks:
    for segment in track.segments:
      line = []
      for point in segment.points:
        line.append((point.latitude, point.longitude, point.elevation))
      lines.append(line)
  for route in gpx.routes:
    line = []
    for point in route.points:
      line.append((point.latitude, point.longitude, point.elevation))
    lines.append(line)

  # fallback to waypoints
  if len(lines) == 0:
    for point in gpx.waypoints:
      line = [(point.latitude, point.longitude, point.elevation)]
      lines.append(line)

  return lines


def reduced_lines(original_lines, max_vertices):
  lines = []
  for original_line in original_lines:
    total_vertices = len(original_line)
    max_vertices = min(max_vertices, total_vertices)
    step = int(total_vertices / max_vertices)
    line = []
    for i in range(0, len(original_line) - 1, step):
      line.append(original_line[i])
      line.append(original_line[-1])
    lines.append(line)
  return lines
