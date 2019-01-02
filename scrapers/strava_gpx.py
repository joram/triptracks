#!/usr/bin/env python
import os
import time
from stravalib.client import Client as StravaClient


class StravaGPX(object):

    GOT_ACTIVITY_IDS = []

    def run(self, access_tokens):
        for access_token in access_tokens:
            client = StravaClient(access_token=access_token)
            for activity in self.activities(client):
                if self.cached(activity.id):
                    print "cached: ", activity.name
                else:
                    yield activity, client.get_gpx_file(activity.id)
                time.sleep(5)

    def cached(self, activity_id):
        return activity_id in self.GOT_ACTIVITY_IDS

    def files(self):
        for filename in os.listdir(self.storage_dir()):
            yield os.path.join(self.storage_dir(), filename)

    def activities(self, client):
        for filename in os.listdir(self.storage_dir()):
            activity_id, _ = filename.split("_")
            self.GOT_ACTIVITY_IDS.append(int(activity_id))

        after = None
        while True:

            last_activity = None
            for activity in client.get_activities(after=after):
                yield activity
                last_activity = activity

            if last_activity is not None:
                after = last_activity.start_date

    def storage_dir(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, "../data/StravaGPX")

    def write(self, filepath, data):
        directory = os.path.dirname(os.path.realpath(filepath))
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, "w") as f:
            f.write(data)


if __name__ == "__main__":
    s = StravaGPX()
    for activity, data in s.run(access_tokens=[]):
        try:
            filepath = "{}/{}_{}.gpx".format(s.storage_dir(), activity.id, activity.name)
            print filepath
            if data is not None:
                s.write(filepath, data)
        except:
            print activity.name