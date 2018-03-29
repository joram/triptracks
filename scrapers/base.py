#!/usr/bin/python
import os
import re
import time
import requests
import json
from BeautifulSoup import BeautifulSoup
import HTMLParser

parser = HTMLParser.HTMLParser()


class FailedRequest(Exception):
    pass


class BaseScraper(object):
    FILETYPE = "json"

    def __init__(self):
        self.debug = False
        self.wait = 1
        self.items_count = 0
        self._data_dir = None
        self._data_raw_dir = None
        self.base_url = ""

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

    @property
    def data_raw_dir(self):
        if self._data_raw_dir is None:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            data_raw_dir = os.path.join(dir_path, "../data_raw/", self.__class__.__name__, "./")
            data_raw_dir = os.path.abspath(data_raw_dir)
            if not os.path.exists(data_raw_dir):
                os.makedirs(data_raw_dir)
            self._data_raw_dir = data_raw_dir
        return self._data_raw_dir

    def item_filepath(self, id, ):
        if not id.endswith(".{}".format(self.FILETYPE)):
            id += ".{}".format(self.FILETYPE)
        filepath = os.path.join(self.data_dir, "./{}".format(id))
        filepath = os.path.abspath(filepath)
        return filepath

    def have_item(self, id):
        return os.path.exists(self.item_filepath(id))

    def store_item(self, id, data):
        with open(self.item_filepath(id), "w") as f:
            f.write(data)

    def item_urls(self):
        raise NotImplemented()

    def item_content(self, url, id):
        raise NotImplemented()

    def get_content(self, url, extension="html"):
        cache_filepath = os.path.join(self.data_raw_dir, url.replace(self.base_url, "")).rstrip("/")
        extension = ".{}".format(extension)
        if not cache_filepath.lower().endswith(extension):
            cache_filepath += extension

        if os.path.exists(cache_filepath):
            print "loading cached {}".format(url)
            with open(cache_filepath) as f:
                return f.read()

        print "downloading {}".format(url)
        time.sleep(self.wait)
        resp = requests.get(url)
        if resp.status_code != 200:
            raise FailedRequest()

        cache_path = os.path.dirname(cache_filepath)
        cache_path = os.path.abspath(cache_path)
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        with open(cache_filepath, "w+") as f:
            f.write(resp.content)

        return resp.content

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
        for id, url in self.item_urls():
            if not self.have_item(id):
                try:
                    filename, data = self.item_content(url, id)
                    if data is None:
                        raise FailedRequest()
                    if self.debug:
                        print filename, url
                    self.store_item(filename, data)
                except:
                    self.store_item(id+"____FAILED", "")

    def items(self):
        for id, url in self.item_urls():

            try:
                filename, data = self.item_content(url, id)
                filepath = self.item_filepath(filename)
                if data is None:
                    raise FailedRequest()
                self.store_item(filename, data)
                yield id, filepath, data
            except Exception as e:
                print e
                self.store_item(id+"____FAILED", "")
            continue

