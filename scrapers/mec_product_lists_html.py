#!/usr/bin/python
from base import BaseScraper
import os
import json


class ScrapeMECProductListHtml(BaseScraper):

    def __init__(self):
        super(ScrapeMECProductListHtml, self).__init__()
        self.base_url = "http://www.mec.ca/"
        self.root_url = "http://www.mec.ca/shop/"
        self.visited_shop_urls = []
        self.unvisited_shop_urls = []
        self.product_urls = []
        self._existing_urls = None
        self._existing_files = None

    def _is_category_url(self, url):
        # https://www.mec.ca/en/products/footwear/c/1184
        if "?" in url:
            return False
        if not url.startswith(" https://www.mec.ca/en/products/"):
            return False
        return True

    def _category_id(self, url):
        url = url.replace(" https://www.mec.ca/en/products/")
        return int(url.split("/")[-1])

    def item_content(self, url):
        return self.get_content(url)

    def item_cache_filepath(self, url):
        id = self._category_id(url)
        id = str(id).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.html".format(id)))

    def item_urls(self):
        self.unvisited_shop_urls.append(self.root_url)
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
                id = product_url.split("/")[-1]

                yield id, product_url


if __name__ == "__main__":
    s = ScrapeMECProductListHtml()
    s.debug = True
    s.run()
