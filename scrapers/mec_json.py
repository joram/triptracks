#!/usr/bin/env python
from base import BaseScraper
from mec_raw_html import ScrapeMEC
import os
import json


class ScrapeMECJSON(BaseScraper):

    def __init__(self, debug=False):
        BaseScraper.__init__(self, debug)
        self.html_scraper = ScrapeMEC(False)
        self._existing_files = None

    def item_cache_filepath(self, url):
        product_id = 0
        if url != "http://www.mec.ca/shop/":
            product_id = url.replace(self.base_url, "").split("/")[-1]
        p = os.path.abspath(os.path.join(self.data_dir, "./{}.json".format(product_id)))
        return p

    def item_urls(self):
        for url in self.html_scraper.item_urls():
            yield url

    def _details(self, soup, data):
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
        return data

    def get_uncached_content(self, url):
        if url == "http://www.mec.ca/shop/":
            self.store_item(self.item_cache_filepath(url), {})
            return {}
        soup = self.html_scraper.get_soup(url)
        data = self.html_scraper.get_metadata(soup)
        data = self._details(soup, data)
        data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

        self.store_item(self.item_cache_filepath(url), data)
        return data


if __name__ == "__main__":
    s = ScrapeMECJSON(True)
    for data in s.run():
        data = json.loads(data)
        w = None
        for k in ["Weight", "weight"]:
            w = data.get(k)
            if w is not None:
                break
        print ("weight: %s" % w).ljust(70, " ") + data.get("title", "???")
