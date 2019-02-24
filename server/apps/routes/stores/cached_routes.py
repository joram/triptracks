import json
import boto3
import os


class CachedRoutesStore(object):

  def __init__(self, max_vertices, base_store):
    self.client = boto3.client('s3')
    self.bucket = "triptracks"
    self.base_path = os.path.join("routes/cache", str(max_vertices))
    self.base_store = base_store
    self.max_vertices = max_vertices
  
  def get(self, geohash):
    from apps.routes.models import Route
    path = os.path.join(self.base_path, "{}.json".format(geohash))
    content = self._get_s3_content(path)
    if content is not None:
      content = json.loads(content)
      routes = [Route(pub_id=r["pub_id"], name=r["name"], lines=r["lines"]) for r in content]
      return routes

    print("building cache key")
    routes = []
    for r in self.base_store.get(geohash):
        routes.append({
          "pub_id": r.pub_id,
          "name": r.name,
          "lines": r.vertices(self.max_vertices),
        })
    self._write_s3_content(path, json.dumps(routes))
    return self.get(geohash)

  def get_by_pub_id(self, pub_id):
    route = self.base_store.get_by_pub_id(pub_id)
    print("cached getting ", route)
    return route

  def _write_s3_content(self, key, content):
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name=self.bucket, key=key)
    object.put(Body=content)

  def _get_s3_content(self, key=''):
    try:
        obj = self.client.get_object(Bucket=self.bucket, Key=key)
        content = obj['Body'].read()
        return content
    except self.client.exceptions.NoSuchKey:
        return None
