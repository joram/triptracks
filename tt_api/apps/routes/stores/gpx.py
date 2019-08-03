from apps.routes.stores.base import BaseS3Store


class GPXS3Store(BaseS3Store):

    def __init__(self):
        BaseS3Store.__init__(self)
        self.base_path = "routes/gpx"
