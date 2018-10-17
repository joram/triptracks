#!/usr/bin/env python
from base import BaseScraper
import os
import json


class ScrapeMEC(BaseScraper):

    def __init__(self, debug=False):
        BaseScraper.__init__(self, debug)
        self.base_url = "http://www.mec.ca/"
        self.visited_shop_urls = []
        self.unvisited_shop_urls = []
        self.product_urls = []
        self._existing_urls = None
        self._existing_files = None

    @property
    def existing_files(self):
        if self._existing_files is None:
            self._existing_files = os.listdir(self.data_dir)
        return self._existing_files

    def item_cache_filepath(self, url):
        product_id = 0
        if url != "http://www.mec.ca/shop/":
            parts = url.replace(self.base_url, "").split("/")
            product_id = url.replace(self.base_url, "").split("/")[-1]
        p = os.path.abspath(os.path.join(self.data_dir, "./{}.html".format(product_id)))
        return p

    def item_urls(self):
        self.unvisited_shop_urls.append("http://www.mec.ca/shop/")
        while self.unvisited_shop_urls:
            url = self.unvisited_shop_urls.pop()
            self.visited_shop_urls.append(url)
            soup = self.get_soup(url)
            hrefs = set([a['href'] for a in soup.findAll('a', href=True)])
            for href in hrefs:
                href = "http://www.mec.ca%s" % href if not href.startswith(self.base_url) else href
                if "?" in href:
                    href = href.split("?")[0]

                # handle more shop urls
                if href.startswith("http://www.mec.ca/en/products/") and href not in self.visited_shop_urls:
                    self.unvisited_shop_urls.append(href)
                    continue

                href = href.split("?")[0]
                product_url = href.split("#")[0]
                if product_url in self.product_urls:
                    continue
                if not product_url.startswith("http://www.mec.ca/en/product/"):
                    continue
                if "gift-card" in product_url.lower():
                    continue

                self.product_urls.append(product_url)
                yield product_url

    def get_existing_content(self, id):
        for filename in self.existing_files:
            if filename.startswith(id):
                filepath = self.item_filepath(id)
                with open(filepath) as f:
                    data = f.read()
                    return data
        return None

    def item_content(self, url, id):
        data = self.get_existing_content(id)
        if data is not None:
            return id, data

        soup = self.get_soup(url)
        data = self.get_metadata(soup)

        # specs
        try:
            data['price'] = soup.find("li", {"class": "price"}).text
        except:
            data["price"] = "N/A"

        primary_img_div = soup.find("div", {"id": "primary_image"})
        imgs = primary_img_div.findAll("img", {"class": "srcset-image__content"})
        data["img_href"] = imgs[0]["src"]

        specs = soup.find(id="pdp-tech-specs")
        if specs:
            for tr in specs.findAll("tr"):
                th = tr.find("th")
                td_a = th.find("a")
                td = tr.find("td")
                if td and th:
                    key = th.text
                    if key is "":
                        continue
                    if td_a:
                        key = td_a.find(text=True, recursive=False).rstrip("\r\n ")
                    val = td.text
                    data[key] = val

        return id, json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def filepaths(self):
        existing_files = os.listdir(self.data_dir)
        for filename in existing_files:
            filepath = os.path.join(self.data_dir, filename)
            yield filepath


if __name__ == "__main__":
    s = ScrapeMEC(True)
    for c in s.run():
        pass
