#!/usr/bin/python
import os
from base import BaseScraper
from BeautifulSoup import BeautifulSoup


class ScrapeTrailPeak(BaseScraper):
    FILETYPE = "gpx"
    existing_ids = {}

    def item_urls(self):

        existing_files = os.listdir(self.data_dir)
        for filename in existing_files:
            id = filename.split("_")[0]
            try:
                self.existing_ids[int(id)] = True
            except:
                pass

        for i in range(1, 100000):
            yield str(i), "https://www.trailpeak.com/index.jsp?con=trail&val={}".format(i)

    def _get_existing_content(self, id):
        if self.existing_ids.get(int(id), False):
            existing_files = os.listdir(self.data_dir)
            for filename in existing_files:
                if filename.startswith("{}_".format(id)):
                    filepath = os.path.join(self.data_dir, filename)
                    print "EXISTS: {}".format(filename)
                    with open(filepath) as f:
                        return filename, f.read()
        return None, None

    def _get_new_content(self, url, id):
        content = self.get_content(url)
        soup = BeautifulSoup(content)
        title = soup.title.string.split("near")[0].lstrip(" ").rstrip(" ").replace(" ", "_")
        filename = "{}_{}".format(id, title).replace("/", "")
        filepath = os.path.join(self.data_dir, filename)

        for line in content.split("\n"):
            if "GPX_URL" in line:
                name = line.split("\"")[1]
                gpx_url = "https://www.trailpeak.com/content/gpsData/gps{}-{}.gpx".format(id, name)

                data = self.get_content(gpx_url)
                self.store_item(filename, data)
                print "FETCHED: {} ".format(filename)
                return filename, data

    def item_content(self, url, id):
        filename, data = self._get_existing_content(id)
        if filename is None:
            filename, data = self._get_new_content(url, id)
        return filename, data

    def filepaths(self):
        existing_files = os.listdir(self.data_dir)
        for filename in existing_files:
            filepath = os.path.join(self.data_dir, filename)
            if filename.endswith(".gpx") and not filename.endswith("FAILED.gpx"):
                yield filepath


if __name__ == "__main__":
    s = ScrapeTrailPeak()
    s.debug = True
    s.run()
