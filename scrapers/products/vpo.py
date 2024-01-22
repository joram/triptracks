#!/usr/bin/env python
import atexit
import dataclasses
import json
import os

from scrapers.base import BaseScraper
from products.models.product import Spec, Product
from scrapers.utils.sitemap import get_sitemap_urls
from scrapers.utils.opengraph import parse as parse_og


class VPOScraper(BaseScraper):

    def __init__(self):
        super().__init__()
        self.wait = 0
        self.sold_out = []
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = f"./vpo_sold_out.json"
        self.sold_out_filepath = os.path.abspath(os.path.join(curr_dir, filepath))
        if os.path.exists(self.sold_out_filepath):
            with open(self.sold_out_filepath, "r") as f:
                self.sold_out = json.load(f)

    def save_sold_out(self):
        print("Saving sold out")
        with open(self.sold_out_filepath, "w") as f:
            json.dump(self.sold_out, f, indent=2, sort_keys=True)

    def item_urls(self):
        sitemap = get_sitemap_urls("https://www.vpo.ca")
        for url in sitemap:
            if "/product/" in url:
                yield url

    def mark_as_sold_out(self, url):
        self.sold_out.append(url)

    def get_product(self, url):
        if url in self.sold_out:
            return None

        filepath = self.item_cache_filepath(url).replace(".html", ".json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
                data = json.loads(content)
                return Product(**data)

        soup = self.get_soup(url)
        try:
            availability = soup.find("div", {"itemprop": "availability"}).text.strip()
            if availability.lower() == "out of stock":
                self.mark_as_sold_out(url)
        except:
            pass

        script = soup.find("script", {"id": "modelData"})
        if script is not None:
            data = json.loads(script.text)
            product = Product(
                name=data["name"],
                description=data["description"],
                url=url,
                price_cents=data["price"],
                img_hrefs=[data["image"]],
                specs=[Spec(key="weight", value=data["weight"])],
            )
            return product

        og_data = parse_og(soup)

        price_cents = None
        price_span = soup.find("span", {"id": "VPO_Price"})
        if price_span is not None:
            s = price_span.text.strip().replace("$", "").replace(".", "")
            if s == "":
                s = "0"
            if "-" in s:
                s = s.split("-")[0].strip()
            price_cents = int(s)*100

        def _get_specs():
            spec_p = soup.find("p", {"id": "specsId"})
            if spec_p is not None:
                specs = []
                content = str(spec_p)
                content = content.replace("<br>", "\n")
                content = content.replace("<br/>", "\n")
                content = content.replace("<p id=\"specsId\">", "")
                content = content.replace("</p>", "")
                lines = content.split("\n")
                for line in lines:
                    if ":" in line:
                        parts = line.split(":")
                        key = parts[0].strip("* ")
                        value = parts[1].strip().split("/")[0].strip()
                        if value == "":
                            continue
                        specs.append(Spec(key=key, value=value))
                return specs
            return []

        try:
            return Product(
                name=og_data["title"].replace(" | FREE SHIPPING in Canada |", ""),
                description=og_data["description"],
                url=url,
                price_cents=price_cents,
                img_hrefs=[og_data["image"]],
                specs=_get_specs(),
            )
        except:
            return None

    def products(self):
        for url in ["https://vpo.ca/product/301460/sirocco-helmet"]:
            yield self.get_product(url), url
        for url in self.item_urls():
            yield self.get_product(url), url


if __name__ == "__main__":
    s = VPOScraper()

    atexit.register(s.save_sold_out)

    i = 0
    for item, url in s.products():
        if item is None:
            print(f"{i}\t None\t {url}")
            i +=1
            continue
        print(f"{i}\t {item.price_cents}".ljust(10), item.name, item.url)

        filepath = os.path.join(s.data_dir, f"../../products/data/vpo/{item.slug}.json")
        filepath = os.path.abspath(filepath)
        directory = os.path.dirname(filepath)
        os.makedirs(directory, exist_ok=True)

        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump(dataclasses.asdict(item), f, indent=2, sort_keys=True)
        i += 1
