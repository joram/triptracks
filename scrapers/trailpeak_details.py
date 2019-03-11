#!/usr/bin/python
import os
from scrapers.base import BaseScraper
from bs4 import BeautifulSoup
import json
from trailpeak_gpx import ScrapeTrailPeakGPX


class ScrapeTrailPeakRawHTML(BaseScraper):

    def __init__(self):
        BaseScraper.__init__(self)
        self.base_url = "https://www.trailpeak.com/index.jsp?con=trail&val="

    def item_urls(self):
        for i in range(1, 14000):
            yield f"https://www.trailpeak.com/index.jsp?con=trail&val={i}"

    def item_content(self, url):
        return self.get_content(url)

    def item_cache_filepath(self, url):
        id = int(url.replace(self.base_url, ""))
        id = str(id).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.html".format(id)))


class ScrapeTrailPeakDetails(BaseScraper):

    def __init__(self, debug):
        BaseScraper.__init__(self)
        self.html_scraper = ScrapeTrailPeakRawHTML()
        self.gpx_scraper = ScrapeTrailPeakGPX()
        self.html_scraper.debug = debug
        self.debug = debug
        self.base_url = "https://www.trailpeak.com/index.jsp?con=trail&val="
        self.wait = 0

    def item_urls(self):
        for i in range(1, 100000):
            yield f"https://www.trailpeak.com/index.jsp?con=trail&val={i}"

    def get_uncached_content(self, url):
        trail_id = url.replace(self.base_url, "")
        html = self.html_scraper.item_content(url)
        if "Sorry, the trail you request could not be found" in html:
            return json.dumps({})
        bs = BeautifulSoup(html)

        description = ""
        descDiv = bs.find("div", {"id": "description"})
        if descDiv is not None:
            for p in descDiv.findAll("p"):
                description += p.text
            description = description.rstrip("Advertisement:")

        directions = ""
        if "Directions:" in description:
            description, directions = description.split("Directions:")

        name = "trail: {}".format(trail_id)
        try:
            name = bs.find("div", {"class": "TableHeader"}).find("h1").text
        except:
            pass

        image_url = ""
        try:
            image_url = bs.find("img", {"alt": "trail-image"}).attrMap["src"]
        except:
            pass

        self.gpx_scraper.get_content(url)
        details = {
            "description": description,
            "directions": directions,
            "name": name,
            "trail_id": trail_id,
            "trail_image_url": image_url,
            "url": url,
            "gpx_filepath": self.gpx_scraper.item_filepath(trail_id),
        }
        return json.dumps(details, sort_keys=True, indent=4, separators=(',', ': '))

    def item_cache_filepath(self, url):
        id = int(url.replace(self.base_url, ""))
        id = str(id).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.json".format(id)))


if __name__ == "__main__":
    s = ScrapeTrailPeakDetails(True)
    for route in s.json_items():
        print(route.keys())
