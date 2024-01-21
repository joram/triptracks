#!/usr/bin/env python
import dataclasses

from base import BaseScraper
from mec_raw_html import ScrapeMEC
import os
import json

from scrapers.products.models.product import Spec, Product
from scrapers.utils.sitemap import get_sitemap_urls


class ScrapeMECJSON(BaseScraper):

    base_url = "https://www.mec.ca/en/"

    def __init__(self, debug=False):
        BaseScraper.__init__(self, debug)
        self.html_scraper = ScrapeMEC(False)
        self._existing_files = None

    def item_urls(self):
        sitemap = get_sitemap_urls("https://www.mec.ca/en/")
        for url in sitemap:
            if "/product/" in url:
                yield url

    def item_cache_filepath(self, url):
        url = url.rstrip("/")
        url = url.replace("https://", "").replace("http://", "").replace("/", "_").rstrip("/")
        url = url.replace("?", "_").replace("=", "_").replace("&", "_")
        filepath = os.path.join(self.data_dir, "./{}".format(url))
        filepath = os.path.abspath(filepath)
        return filepath

    def get_product(self, url) -> Product:
        filepath = self.item_cache_filepath(url).replace(".html", ".json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
            return Product(**data)

        soup = self.html_scraper.get_soup(url)
        data = soup.find("script", {"id": "__NEXT_DATA__"}).text
        data = json.loads(data)

        def find_key(data, path, key):
            if isinstance(data, dict):
                for k, v in data.items():
                    if k == key:
                        return v
                    else:
                        path.append(k)
                        result = find_key(v, path, key)
                        if result is not None:
                            return result
                        path.pop()
            elif isinstance(data, list):
                for i, v in enumerate(data):
                    path.append(i)
                    result = find_key(v, path, key)
                    if result is not None:
                        return result
                    path.pop()
            return None

        product = find_key(data, [], "product")

        def _get_price_cents():
            values = []
            if "variants" in product:
                variants = product["variants"]
                if len(variants) == 1:
                    variant = variants[0]
                    price = variant.get("price")
                    if price is None:
                        price = variant.get("lowPrice")
                    if price is None:
                        price = variant.get("highPrice")
                    values.append(price.get("value"))

            price_data = product.get("price", {})
            for key in price_data.keys():
                try:
                    value = price_data[key].get("value")
                except Exception:
                    continue
                if value is not None:
                    values.append(value)

            values = [float(value) for value in values if value is not None]
            min_price = min(values)
            price_cents = int(min_price * 100)
            return price_cents

        def _get_image_urls():
            image_urls = []
            for image in product.get("images", []):
                image_urls.append(image.get("urlOriginal"))
            return image_urls

        def _get_specs():
            specs = []
            for spec in product.get("techSpecs", []):
                key = spec.get("key")
                if "/>" in spec.get("value"):
                    for value in spec.get("value").split("<br/>"):
                        if "(" in value:
                            parts = value.split("(")
                            value = parts[0].strip()
                            extra_key = parts[1].replace(")", "").strip()
                            specs.append(Spec(key=f"{key} ({extra_key})", value=value))
                        else:
                            specs.append(Spec(key=key, value=value))
                else:
                    specs.append(Spec(key=key, value=spec.get("value")))
            return specs

        product = Product(
            name=product.get("name"),
            url=url,
            price_cents=_get_price_cents(),
            img_hrefs=_get_image_urls(),
            specs=_get_specs(),
        )

        with open(filepath, "w") as f:
            json.dump(dataclasses.asdict(product), f)
        return product

    def products(self):
        for url in self.item_urls():
            yield self.get_product(url)


if __name__ == "__main__":
    s = ScrapeMECJSON(True)
    for item in s.products():
        print(f"{item.price_cents/100}".ljust(10), item.name, item.url)
