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
from common.scrapers.base import Scrape
from django.conf import settings
parser = HTMLParser.HTMLParser()


class ScrapeMEC(Scrape):

	def __init__(self):
		super(ScrapeMEC, self).__init__()
		self.base_url = "http://www.mec.ca/"
		self.visited_shop_urls = []
		self.unvisited_shop_urls = []
		self.visited_product_urls = []
		self.data_dir = os.path.join(settings.BASE_DIR, "../data/mec")

	def shop_json(self, url):

		# json filepath
		filepath = os.path.join(self.data_dir, 'shop_json')
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
		soup = self.get_soup(url)
		data = [a['href'] for a in soup.findAll('a', href=True)]
		if data:
			if not os.path.exists(os.path.dirname(filepath)):
			    os.makedirs(os.path.dirname(filepath))
			with open(filepath, "w") as f:
				json_str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
				f.write(json_str)

		return data	

	def item_urls(self):
		self.unvisited_shop_urls.append("http://www.mec.ca/shop/")
		while self.unvisited_shop_urls:
			# maintain visited/visiting lists
			url = self.unvisited_shop_urls.pop()
			self.visited_shop_urls.append(url)
			hrefs = self.shop_json(url)
			for href in hrefs:
				href = "http://www.mec.ca%s" % href if not href.startswith(self.base_url) else href
				
				# handle more shop urls
				if href.startswith("http://www.mec.ca/shop/") and href not in self.visited_shop_urls:
					self.unvisited_shop_urls.append(href)

				# handle products
				product_url = href.split("?")[0]
				if product_url not in self.visited_product_urls and \
					product_url.startswith("http://www.mec.ca/product/") and \
					"gift-card" not in product_url:
						self.visited_product_urls.append(product_url)
						yield product_url

	def item_data(self, url):

		self.visited_product_urls.append(url)
		soup = self.get_soup(url)	
		if soup:
			try:
				data = {
					'url': url,
					'description': soup.find(id='gearNotes').text,
					'name': soup.find(id="shopbox").find("h1").text,
					'price': soup.find(id="idPrdPrice").text,
					'img_href': soup.find(id='zoom1')['href'],
				}

				specs = soup.find(id="specchart")
				if specs:
					for tr in specs.findAll("tr"):
						th = tr.find("th")
						td_a = th.find("a")
						td = tr.find("td")
						if td and th:
							key = th.text
							if td_a:
								key = td_a.find(text=True, recursive=False).rstrip("\r\n ")
							val = td.text
							data[key] = val

				return data
			except AttributeError as e:
				print url
				print e


def push_item(data):
	for k in data.keys():
		try:
			data[k] =  parser.unescape(str(data[k]))
		except Exception as e:
			print e
	price = data.get('price', '').replace("$", "").replace(" ", "")
	if "CAD" in price:
		price = price.split("CAD")[0]
	if "-" in price:
		price = price.split("-")[1]
	price = float(price) if price != '' else -1

	massaged_data = {
		'name': data.get('name'),
		'price': price,
		'description': data.get('description'),
		'attributes': data}

	r = requests.post(
		url="http://localhost:8000/api/v1/item/",
	    data=json.dumps(massaged_data),
	    headers={
	    	'Content-type': 'application/json',
	    	'Accept': 'text/plain'}
	)
	return r.status_code

