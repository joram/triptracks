from routes.models.route import Route
import os
import boto3
import json


class S3RoutesStore(object):
    
  def __init__(self):
    self.bucket = "triptracks"
    self.base_path = "routes/raw"

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

  def add(self, route):
    key = os.path.join(self._path(route.geohash()), "{}.json".format(route.pub_id))
    print("adding {}".format(key))
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name=self.bucket, key=key)
    object.put(Body=json.dumps(route.details()))

  def _path(self, geohash):
    return os.path.join(self.base_path, "/".join(geohash))

  def _get_s3_content(self, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(self.bucket, key)
    return obj.get()['Body'].read().decode('utf-8')

  def _get_matching_s3_keys(self, prefix=''):
    # s3 = boto3.resource('s3')
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