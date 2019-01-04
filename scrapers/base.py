import os
import re
import time
import requests
from bs4 import BeautifulSoup


class FailedRequest(Exception):
    pass


class BaseScraper(object):
    FILETYPE = "json"

    def __init__(self, debug=False):
        self.debug = debug
        self.wait = 1
        self.items_count = 0
        self._data_dir = None
        self._data_raw_dir = None
        self.base_url = ""
        self.extension = "html"

    @property
    def data_dir(self):
        if self._data_dir is None:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            data_dir = os.path.join(dir_path, "../data/", self.__class__.__name__, "./")
            data_dir = os.path.abspath(data_dir)
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            self._data_dir = data_dir
        return self._data_dir

    def item_filepath(self, id):
        if not id.endswith(".{}".format(self.FILETYPE)):
            id += ".{}".format(self.FILETYPE)
        filepath = os.path.join(self.data_dir, "./{}".format(id))
        filepath = os.path.abspath(filepath)
        return filepath

    def have_item(self, filepath):
        return os.path.exists(filepath)

    def store_item(self, filepath, data):
        with open(filepath, "wb") as f:
            f.write(data)

    def get_item(self, filepath):
        with open(filepath, "r") as f:
            return f.read()

    def item_urls(self):
        raise NotImplemented()

    def item_cache_filepath(self, url):
        raise NotImplemented()

    def get_uncached_content(self, url):
        if self.debug:
            print("downloading {}".format(url))
        time.sleep(self.wait)
        resp = requests.get(url)
        if resp.status_code != 200:
            raise FailedRequest(resp.content)
        return resp.content

    def get_content(self, url):

        # check cache
        cache_filepath = self.item_cache_filepath(url)
        if self.have_item(cache_filepath):
            if self.debug:
                print("loading cached {}".format(url))
            return self.get_item(cache_filepath)

        content = self.get_uncached_content(url)

        # update cache
        path = os.path.dirname(cache_filepath)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(cache_filepath, "w+") as f:
            f.write(content)

        return content

    def get_soup(self, url):
        html = self.get_content(url)
        soup = BeautifulSoup(html)
        return soup

    def get_metadata(self, soup):
        data = {}

        # opengraph data
        for tag in soup.findAll(property=re.compile(r'^og')):
            key = tag["property"].replace("og:", "")
            val = tag["content"]
            data[key] = val

        # facebook data
        for tag in soup.findAll(property=re.compile(r'^fb')):
            key = tag["property"].replace("fb:", "")
            val = tag["content"]
            data[key] = val

        return data

    def run(self):
        for url in self.item_urls():
            try:
                yield self.get_content(url)
            except Exception as e:
                print(e)
                pass

