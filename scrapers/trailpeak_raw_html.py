#!/usr/bin/python
import os
from scrapers.base import BaseScraper


class ScrapeTrailPeakRawHTML(BaseScraper):

    def __init__(self):
        BaseScraper.__init__(self)
        self.base_url = "https://www.trailpeak.com/index.jsp?con=trail&val="

    def item_urls(self):
        for i in range(1, 14000):
            yield "{}{}".format(self.base_url, i)
            break

    def item_content(self, url):
        return self.get_content(url)

    def item_cache_filepath(self, url):
        id = int(url.replace(self.base_url, ""))
        id = str(id).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.html".format(id)))


if __name__ == "__main__":
    s = ScrapeTrailPeakRawHTML()
    s.debug = True
    s.run()
