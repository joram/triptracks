import os
import boto3
import requests


class BaseS3Store(object):

  def __init__(self):
    self.bucket = "triptracks"
    self.base_path = None

  def get(self, filename):
    return self._get_s3_content(self._get_key(filename))

  def put(self, filename, content):
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name=self.bucket, key=self._get_key(filename))
    object.put(Body=content)

  def put_by_url(self, filename, url):
    resp = requests.get(url)
    if resp.status_code != 200:
      raise Exception()
    self.put(filename, resp.content)

  def _get_key(self, filename):
    if self.base_path is None:
      raise Exception()
    return os.path.join(self.base_path, filename)

  def _get_s3_content(self, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(self.bucket, key)
    return obj.get()['Body'].read().decode('utf-8')


class GPXS3Store(BaseS3Store):

  def __init__(self):
    BaseS3Store.__init__(self)
    self.base_path = "routes/gpx"


class ImageS3Store(BaseS3Store):

  def __init__(self):
    BaseS3Store.__init__(self)
    self.base_path = "routes/image"
