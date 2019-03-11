#!/usr/bin/env python
import json
import os
from bs4 import BeautifulSoup
from base import BaseScraper
from summitpost_mountain_routes_list import ScrapeSummitPostMountainRoutesList
from summitpost_base import BaseSummitPostScraper


class ScrapeSummitPostRawHTML(BaseScraper):

    def __init__(self):
        BaseScraper.__init__(self)
        self.base_url = "https://www.summitpost.org/undefined-behaviour/"

    def item_urls(self):
        for i in range(1, 14000):
            yield "{}{}".format(self.base_url, i)

    def item_content(self, url):
        html = self.get_content(url)
        return html

    def item_cache_filepath(self, url):
        id = url.split("/")[-1].replace("\\'", "")
        id = int(id)
        id = str(id).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.html".format(id)))


class ScrapeSummitPostDetails(BaseSummitPostScraper):

    def __init__(self, debug=True):
        BaseScraper.__init__(self, debug)
        self.routes_list_scraper = ScrapeSummitPostMountainRoutesList()
        self.route_html_scraper = ScrapeSummitPostRawHTML()
        self.base_url = "https://www.summitpost.org/"

    def item_urls(self):
        for list_urls in self.routes_list_scraper.json_items():
            for route_url in list_urls:
                yield route_url

    def item_cache_filepath(self, url):
        id = int(url.split("/")[-1].replace("\\'", ""))
        id = str(id).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.json".format(id)))

    def get_uncached_content(self, url):
        html = self.route_html_scraper.item_content(url)
        if "This page has been deleted." in html:
            return json.dumps({})

        bs = BeautifulSoup(html, features="lxml")
        if bs.find("div", {"class": "full-content"}) is None:
            return json.dumps({})

        details = {
            "url": url,
            "title": bs.find("h1", {"class": "adventure-title"}).string,
            "description": self._description(bs),
            "details": self._details(bs),
        }
        return json.dumps(details)


if __name__ == "__main__":
    s = ScrapeSummitPostDetails(False)
    for route in s.json_items():
        gpx_file = route.get("details", {}).get("gpx file")
        if gpx_file is not None:
            print("\t", gpx_file, "\t", route.get("title"))
        else:
            print("\t", route.get("title"))
