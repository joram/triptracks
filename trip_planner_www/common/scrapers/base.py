#!/usr/bin/python
import os
import pdb
import pprint
import time
import requests
import json
from BeautifulSoup import BeautifulSoup
import html
import HTMLParser
parser = HTMLParser.HTMLParser()


class Scrape(object):

	def __init__(self):
		self.debug = False
		self.wait = 1
		self.items_count = 0

	def items(self):
		for item_url in self.item_urls():
			data = self.item_json(item_url)
			if data:
				yield data
		
	def get_soup(self, url):
		filepath = os.path.join(self.data_dir, url.replace(self.base_url, ""))
		if filepath.endswith("/"):
			filepath += "index.html"
		if os.path.exists(filepath):
			if self.debug:
				print "visited url"
			f = open(filepath)
			html = f.read()
			soup = BeautifulSoup(html)
			return soup

		if self.debug:
			print "new url"
		time.sleep(self.wait)
		html = requests.get(url).text
		if not os.path.exists(os.path.dirname(filepath)):
		    os.makedirs(os.path.dirname(filepath))
		f = open(filepath, "w")
		f.write(html.encode("utf8"))
		f.close()

		soup = BeautifulSoup(html)
		return soup

	def item_data(self, url):
		raise NotImplemented

	def item_json(self, url):
		self.items_count += 1

		# json filepath
		filepath = os.path.join(self.data_dir, 'product_json')
		filepath = os.path.join(filepath, url.replace(self.base_url, ""))
		if filepath.endswith("/"):
			filepath += "index.html"
		filepath += ".json"

		# get existing data
		if os.path.exists(filepath):
			f = open(filepath)
			data = json.loads(f.read())
			return data

		# new data
		data = self.item_data(url)
		if data:
			data['count'] = self.items_count
			data['filepath'] = filepath
			if not os.path.exists(os.path.dirname(filepath)):
			    os.makedirs(os.path.dirname(filepath))
			with open(filepath, "w") as f:
				json_str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
				f.write(json_str)

		return data	