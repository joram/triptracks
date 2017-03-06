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

class ScrapeMEC(Scrape):

	def __init__(self):
		super(ScrapeMEC, self).__init__()
		self.base_url = "http://www.mec.ca/"
		
		self.visited_shop_urls = []
		self.unvisited_shop_urls = []
		
		self.visited_product_urls = []

		cwd = os.path.dirname(os.path.realpath(__file__))
		self.data_dir = os.path.join(cwd, "../data/mec")

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

s = ScrapeMEC()
for item in s.items():
	status_code = push_item(item)
 	name = item.get("name", "unknown")
 	count = item.get("count", -1)
 	print "%s %s %s %s" % (count, status_code, name[:20], len(item.keys()))
