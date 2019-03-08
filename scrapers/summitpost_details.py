#!/usr/bin/env python
import json
import os
from bs4 import BeautifulSoup
from base import BaseScraper
from summitpost_raw_html import ScrapeSummitPostRawHTML
from summitpost_list_search import ScrapeSummitRoutesSearchRawHTML


class ScrapeSummitPostDetails(BaseScraper):

    def __init__(self, debug=True):
        BaseScraper.__init__(self, debug)
        self.html_scraper = ScrapeSummitPostRawHTML()
        self.list_scraper = ScrapeSummitRoutesSearchRawHTML()
        self.base_url = "https://www.summitpost.org/"

    def item_urls(self):
        for list_url in self.list_scraper.item_urls():
            list_html = self.list_scraper.get_content(list_url)
            bs = BeautifulSoup(list_html)
            cci_thumbs = bs.find_all("a", {"class": "cci-thumb"})
            for thumb in cci_thumbs:
                href = thumb.attrs["href"].replace("\'/", "").replace("\\'", "").replace("\\", "")
                url = self.base_url + href
                yield url

    def item_cache_filepath(self, url):
        id = int(url.split("/")[-1].replace("\\'", ""))
        id = str(id).rjust(5, "0")
        return os.path.abspath(os.path.join(self.data_dir, "./{}.json".format(id)))

    def _description(self, bs):
        description = {}
        descriptionDiv = bs.find("div", {"class": "full-content"})
        section_title = ""
        section_content = []
        for child in descriptionDiv.contents:
            if child.name == "h2":
                if section_title != "":
                    description[section_title] = "\n".join(section_content)
                if child is not None and child.string is not None:
                    section_title = child.string.strip(" ").strip(" ")
                section_content = []
            else:
                if child.string not in [None, "\\n"]:
                    section_content.append(child.string.strip("\\n").strip(" "))
        if section_title != "":
            description[section_title] = "\n".join(section_content)
        return description

    def _details(self, bs):
        details = {}
        table = bs.find("table", {"class": "object-properties-table"})
        rows = table.find_all("tr")
        for tr in rows:
            key = tr.find("th")
            val = tr.find("td")
            if key is not None and key.text is not None:
                if key.text.lower() == "lat/lng:":
                    val = tr.find("a")
                key = key.text.strip("\\n").strip(":").lower()
                if key == "gpx file":
                    val = "https://www.summitpost.org"+val.find("a").attrs["href"]
                else:
                    val = val.text.strip("\\n")
                if key in ["route type", "season"]:
                    val = [route_type.strip(" ") for route_type in val.split(",")]
                if key == "lat/lon":
                    lat, lng = val.split(" / ")

                    lat_val, lat_dir = lat.split("°")
                    lat_val = float(lat_val)
                    if lat_dir == "S":
                        lat_val = lat_val*-1.0

                    lng_val, lng_dir = lng.split("°")
                    lng_val = float(lng_val)
                    if lng_dir == "W":
                        lng_val = lng_val*-1.0

                    val = {"lat": lat_val, "lng": lng_val}

                if key != "":
                    details[key] = val
        return details

    def get_uncached_content(self, url):
        html = self.html_scraper.item_content(url)
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
    print("running details scraper")
    i = 0
    for url in s.item_urls():
        data = s.get_content(url)
        data = json.loads(data)
        gpx_file = data.get("details", {}).get("gpx file", ":(")
        print("\t".join([
            str(i),
            gpx_file,
            data.get("title").ljust(40),
            data.get("details", {}).get("lat/lon").__str__().ljust(40),
            data.get("url"),
        ]))
        i += 1
    print("ran")

