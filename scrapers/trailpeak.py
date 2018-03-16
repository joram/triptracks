#!/usr/bin/python
import os
from base import BaseScraper
from BeautifulSoup import BeautifulSoup


class ScrapeTrailPeak(BaseScraper):
    FILETYPE = "gpx"

    def item_urls(self):
        existing_ids = {}
        existing_files = os.listdir(self.data_dir)
        for filename in existing_files:
            id = filename.split("_")[0]
            try:
                existing_ids[int(id)] = True
            except:
                pass

        for i in range(0, 100000):
            if existing_ids.get(i, False):
                continue
            yield str(i), "https://www.trailpeak.com/index.jsp?con=trail&val={}".format(i)

    def item_content(self, url, id):
        content = self.get_content(url)
        soup = BeautifulSoup(content)
        title = soup.title.string.split("near")[0].lstrip(" ").rstrip(" ").replace(" ", "_")
        filename = "{}_{}".format(id, title).replace("/", "")

        for line in content.split("\n"):
            if "GPX_URL" in line:
                name = line.split("\"")[1]
                gpx_url = "https://www.trailpeak.com/content/gpsData/gps{}-{}.gpx".format(id, name)
                return filename, self.get_content(gpx_url)

        return filename, None


s = ScrapeTrailPeak()
s.debug = True
s.run()
