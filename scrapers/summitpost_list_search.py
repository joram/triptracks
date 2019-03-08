#!/usr/bin/env python
import os
from base import BaseScraper


class ScrapeSummitRoutesSearchRawHTML(BaseScraper):

    def __init__(self):
        BaseScraper.__init__(self)
        self.base_url = "https://www.summitpost.org/undefined-behaviour/"

    def item_urls(self):
        url = "https://www.summitpost.org/object_list.php?search_in=name_only&continent_2=North+America&route_type_2={}&map_2=1&order_type=DESC&object_type=2&orderby=distance&page={}"
        for (activity, num_pages) in [("Hiking", 496), ("Mountaineering", 92)]:
            for page in range(1, num_pages):
                yield url.format(activity, page)

    def item_content(self, url):
        html = self.get_content(url)
        return html

    def item_cache_filepath(self, url):
        import pprint

        route_type = ""
        page = -1
        params = url.split("&")
        for param in params:
            k,v = param.split("=")
            if k == "route_type_2":
                route_type = v
            if k == "page":
                page = v

        page = str(int(page)).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, f"./{route_type}_{page}.html"))
