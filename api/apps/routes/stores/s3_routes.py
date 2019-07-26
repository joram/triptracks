from apps.routes.models import RouteMetadata as Route
import os
import boto3
import json


class S3RoutesStore(object):
    
  def __init__(self):
    self.bucket = "triptracks"
    self.base_path = "routes/raw"
    self.manifiest_filename = "manifest.json"
    self._manifest = None

  def get(self, geohash):
    for key in self._get_matching_s3_keys(self._path(geohash)):
      content = self._get_s3_content(key)
      data = json.loads(content)
      route = Route(
        name=data["name"],
        pub_id=data["pub_id"],
        description=data["description"],
        lines=data["lines"],
      )
      yield route

  def get_manifest(self):
    if self._manifest is None:
      manifest = self._get_s3_content(os.path.join(self.base_path, self.manifiest_filename))
      self._manifest = json.loads(manifest)
    return self._manifest

  def get_by_pub_id(self, pub_id):
    from apps.routes.models.route_metadata import RouteMetadata
    rm = RouteMetadata.objects.get(pub_id=pub_id)
    # filepath = self.route_paths.get(pub_id)
    # if filepath is None:
    #     return None
    #
    # with open(filepath) as f:
    #     content = f.read()
    # data = json.loads(content)
    return Route(
      name=rm.name,
      pub_id=pub_id,
      description=rm.description,
      bounds=rm.bounds,
      # owner_pub_id=data.get("owner_pub_id"),
      # is_public=data.get("is_public", False)
    )

  def add(self, route):
    key = os.path.join(self._path(route.geohash()), "{}.json".format(route.pub_id))
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name=self.bucket, key=key)
    object.put(Body=json.dumps(route.details()))

  def _path(self, geohash):
    return os.path.join(self.base_path, "/".join(geohash))

  def _update_manifest(self):
    routes = {}
    for key in self._get_matching_s3_keys(self.base_path):
      if "route_" in key:
        key = key.replace(self.base_path, "").lstrip("/")
        key, route_uuid = key.split("route_")
        route_uuid = route_uuid.replace(".json", "")
        path = key.split("/")

        pub_id = f"route_{route_uuid}"
        geohash = "".join(path)
        print(geohash, pub_id)
        routes[pub_id] = geohash

    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name=self.bucket, key=os.path.join(self.base_path, self.manifiest_filename))
    object.put(Body=json.dumps(routes))

  def _get_s3_content(self, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(self.bucket, key)
    return obj.get()['Body'].read().decode('utf-8')

  def _get_matching_s3_keys(self, prefix=''):
    s3 = boto3.client('s3')
    kwargs = {'Bucket': self.bucket, 'Prefix': prefix}
    while True:
      resp = s3.list_objects_v2(**kwargs)
      for obj in resp['Contents']:
        key = obj['Key']
        yield key
      try:
        kwargs['ContinuationToken'] = resp['NextContinuationToken']
      except KeyError:
        break
