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
