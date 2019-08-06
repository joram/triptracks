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
    try:
      s3 = boto3.resource('s3')
      obj = s3.Object(self.bucket, key)
      return obj.get()['Body'].read().decode('utf-8')
    except:
      return None


class BaseLocalStore(object):

  def __init__(self, folder):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    self.base_path = os.path.join(dir_path, "../../../../data/%s/" % folder)
    self.base_path = os.path.abspath(self.base_path)
    if not os.path.exists(self.base_path):
        os.makedirs(self.base_path)

  def get(self, filename):
    try:
      with open(os.path.join(self.base_path, filename)) as f:
        return f.read()
    except FileNotFoundError:
      return None

  def put(self, filename, content):
    with open(os.path.join(self.base_path, filename), "w") as f:
      f.write(content)
