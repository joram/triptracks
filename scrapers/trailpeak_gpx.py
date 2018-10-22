#!/usr/bin/python
import os
from base import BaseScraper
from trailpeak_raw_html import ScrapeTrailPeakRawHTML


class ScrapeTrailPeakGPX(BaseScraper):
    def __init__(self):
        BaseScraper.__init__(self)
        self.html_scraper = ScrapeTrailPeakRawHTML()
        self.html_scraper.debug = False
        self.base_url = "https://www.trailpeak.com/index.jsp?con=trail&val="
        self.wait = 0

    def item_urls(self):
        for i in range(1, 100000):
            yield "{}{}".format(self.base_url, i)

    def _trail_id(self, gpx_url):
        gpx_url = gpx_url.replace("https://www.trailpeak.com/content/gpsData/gps", "")
        return int(gpx_url.split("-")[0])

    def get_uncached_content(self, url):
        trail_id = url.replace(self.base_url, "")

        html_url = self.base_url+trail_id
        html = self.html_scraper.item_content(html_url)

        for line in html.split("\n"):
            if "GPX_URL" in line:
                name = line.split("\"")[1]
                if name is not "":
                    gpx_url = "https://www.trailpeak.com/content/gpsData/gps{}-{}.gpx".format(trail_id, name)
                    data = BaseScraper.get_uncached_content(self, gpx_url)
                    return data
        return ""

    def item_cache_filepath(self, url):
        id=url
        for extra in ["https://www.trailpeak.com/content/gpsData/gps", self.base_url]:
            id = id.replace(extra, "")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.gpx".format(id)))


if __name__ == "__main__":
    s = ScrapeTrailPeakGPX()
    s.debug = True
    for data in s.run():
        pass
