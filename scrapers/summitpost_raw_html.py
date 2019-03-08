#!/usr/bin/env python
import os
from base import BaseScraper


class ScrapeSummitPostRawHTML(BaseScraper):

    def __init__(self):
        BaseScraper.__init__(self)
        self.base_url = "https://www.summitpost.org/undefined-behaviour/"

    def item_urls(self):
        for i in range(1, 14000):
            url = "{}{}".format(self.base_url, i)
            print(url)
            yield url

    def item_content(self, url):
        html = self.get_content(url)
        return html

    def item_cache_filepath(self, url):
        id = url.split("/")[-1].replace("\\'", "")
        id = int(id)
        id = str(id).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.html".format(id)))

