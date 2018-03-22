#!/usr/bin/python
from base import BaseScraper
import os


class ScrapeMEC(BaseScraper):

    def __init__(self):
        super(ScrapeMEC, self).__init__()
        self.base_url = "http://www.mec.ca/"

        self.visited_shop_urls = []
        self.unvisited_shop_urls = []
        self.product_urls = []

    def item_urls(self):
        self.unvisited_shop_urls.append("http://www.mec.ca/shop/")
        while self.unvisited_shop_urls:
            url = self.unvisited_shop_urls.pop()
            self.visited_shop_urls.append(url)
            soup = self.get_soup(url)
            hrefs = set([a['href'] for a in soup.findAll('a', href=True)])
            for href in hrefs:
                href = "http://www.mec.ca%s" % href if not href.startswith(self.base_url) else href

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

    def item_content(self, url, id):
        soup = self.get_soup(url)
        data = self.get_metadata(soup)

        # specs
        try:
            data['price'] = soup.find("li", {"class": "price"}).text
        except:
            data["price"] = "N/A"

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

        return id, data

    def filepaths(self):
        existing_files = os.listdir(self.data_dir)
        for filename in existing_files:
            filepath = os.path.join(self.data_dir, filename)
            yield filepath


if __name__ == "__main__":
    s = ScrapeMEC()
    s.debug = True
    s.run()
