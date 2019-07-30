from datetime import datetime
# from yr.libyr import Yr


def get_weather(lat, lng):
    data = {}
    # weather = Yr(location_xyz=(lat, lng, 0))
    #
    # for forecast in weather.forecast():
    #     from_dt = forecast["@from"]
    #     data[from_dt] = forecast.get(from_dt, {})
    #     data[from_dt]["from_dt"] = from_dt
    #
    #     for key in forecast["location"].keys():
    #         if key.startswith("@"):
    #             continue
    #         for second_key in ["@value", "@percent", "@name"]:
    #             value = forecast["location"].get(key, {}).get(second_key)
    #             if value:
    #                 try:
    #                     value = float(value)
    #                 except:
    #                     pass
    #                 data[from_dt][key] = value
    #                 break
    #
    # data = data.values()
    # data = sorted(data, key=lambda k: k['from_dt'])
    return data


class DateForecast(object):

    ICON_DAY_SUNNY = "wi-day-sunny"
    ICON_DAY_SNOW = "wi-day-snow"
    ICON_DAY_SLEET = "wi-day-sleeting"
    ICON_DAY_SHOWERS = "wi-day-showers"
    ICON_DAY_RAIN = "wi-day-rain"
    ICON_DAY_SPRINKLE = "wi-day-sprinkle"
    ICON_DAY_FOG = "wi-day-fog"
    ICON_DAY_CLOUDY = "wi-day-cloudy"

    def __init__(self, date):
        self.minTemperature = None
        self.maxTemperature = None
        self._precipitation = 0.0
        self.date = date

    def amend(self, data):
        new_precipitation = data.get("precipitation", 0)
        self._precipitation += new_precipitation

        new_min_temp = data.get("minTemperature")
        self.minTemperature = min([t for t in [self.minTemperature, new_min_temp] if t is not None])

        new_max_temp = data.get("maxTemperature")
        self.maxTemperature = max([t for t in [self.maxTemperature, new_max_temp] if t is not None])

    @property
    def precipitation(self):
        return float("{:.2f}".format(self._precipitation))

    @property
    def date_friendly(self):
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')
        return self.date.strftime("%a %-d")+suffix(self.date.day)
    @property
    def icon(self):
        is_sprinkly = self.precipitation > 0
        is_rainy = self.precipitation >= 10
        is_showers = self.precipitation >= 30
        is_freezing = self.maxTemperature <= 0
        is_sleeting = self.maxTemperature > 0 and self.minTemperature < 0

        if is_freezing and is_rainy:
            return self.ICON_DAY_SNOW
        if is_sleeting and is_rainy:
            return self.ICON_DAY_SLEET

        if is_showers:
            return self.ICON_DAY_SHOWERS
        if is_rainy:
            return self.ICON_DAY_RAIN
        if is_sprinkly:
            return self.ICON_DAY_SPRINKLE
        return self.ICON_DAY_SUNNY


def get_daily_weather(lat, lng):
    data = {}
    for d in get_weather(lat, lng):
        date = datetime.strptime(d.get("from_dt"), '%Y-%m-%dT%H:%M:%SZ').date()
        if str(date) not in data:
            data[str(date)] = DateForecast(date)
        data[str(date)].amend(d)

    return sorted(data.values(), key=lambda x: x.date)


def get_icons(lat, lng):
    icons = []
    for d in get_weather(lat, lng):
        icons.append((d.get("from_dt"), "wi-day-" + _icon(d)))
    return icons


def _icon(weather):
    return "sunny"
