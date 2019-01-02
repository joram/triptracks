from stores.routes import RoutesStore
import os
import boto3

class S3RoutesStore(RoutesStore):
    
    def __init__(self):
        self.bucket = "triptracks"
        self.base_path = "routes"

    def _path(self, geohash):
        return os.path.join(self.base_path, "/".join(geohash))
    
    def get(self, geohash, cached=True):
        if cached:
            path = os.path.join(self._path(geohash), "cache.json")
            content = self._get_s3_content(path)
            if content is not None:
                return content
    
    def _files_in(self, root_dir):
      path = os.path.join(self.base_path, root_dir)
      for key in self._get_matching_s3_files(path):
        yield key

    def _get_s3_content(self, path=''):
      s3 = boto3.resource('s3')
      obj = s3.Object(bucket, key)
      return obj.get()['Body'].read().decode('utf-8') 

    def _get_matching_s3_keys(self, prefix=''):
      s3 = boto3.resource('s3')
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