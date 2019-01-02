import Geohash

def geohash(bbox):
  ((lat1, lng1), (lat2, lng2)) = bbox
  h1 = Geohash.encode(lat1, lng1)
  h2 = Geohash.encode(lat2, lng2)
  i = 0
  for c in h1:
    if h2[i] == c:
      i += 1
  matching = h1[:i]
  return matching
