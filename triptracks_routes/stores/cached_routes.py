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
    path = os.path.join(self.base_path, "{}.json".format(geohash))
    content = self._get_s3_content(path)
    if content is not None:
      content = json.loads(content)
      return content, True

    full_routes = self.base_store.get(geohash)
    routes = []
    for r in full_routes:
        routes.append({
          "pub_id": r.pub_id,
          "name": r.name,
          "lines": r.vertices(self.max_vertices),
        })

    self._write_s3_content(path, json.dumps(routes))
    return routes, False

  def _write_s3_content(self, key, content):
    obj = self.client.put_object(Bucket=self.bucket, Key=key, Body=content)

  def _get_s3_content(self, key=''):
    try:
        obj = self.client.get_object(Bucket=self.bucket, Key=key)
        content = obj['Body'].read()
        return content
    except self.client.exceptions.NoSuchKey:
        return None
