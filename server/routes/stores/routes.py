import os
import json
from routes.models.route import Route


class RoutesStore(object):

    MAX_VERTICES = {
      0: 1,
      1: 10,
      2: 20,
      3: 50,
      4: 100,
      5: 500,
    }

    def __init__(self):
        d = os.path.dirname(os.path.realpath(__file__))
        self.dir = os.path.join(d, "../../../data/routes_store/")
        self.count = 0
        self.route_paths = {}

    def _path(self, geohash):
        return os.path.join(self.dir, "/".join(geohash))

    def add(self, route):
        if route._geohash().endswith("000"):
            return
        self.count += 1
        path = self._path(route._geohash())
        filepath = os.path.join(path, route.pub_id)+".json"

        self.route_paths[route.pub_id] = filepath

        if not os.path.exists(path):
            os.makedirs(path)

        if os.path.exists(filepath):
            print(u"exists {}\t {}".format(self.count, route))
            return

        print(u'adding {}\t {}'.format(
                self.count,
            route.__str__(),
        ))

        with open(filepath, "w") as f:
            f.write(json.dumps(route.details()))

    def get(self, geohash):
        path = self._path(geohash)
        if not os.path.exists(path):
            return

        for filepath in self._files_in(path):
            with open(filepath) as f:
                content = f.read()
            data = json.loads(content)
            yield Route(
              name=data["name"],
              pub_id=data["pub_id"],
              description=data["description"],
              lines=data["lines"],
              # gpx=data["gpx"],
            )

    def get_by_pub_id(self, pub_id):
        print(pub_id)
        print(self.route_paths)
        filepath = self.route_paths.get(pub_id)
        if filepath is None:
            return None

        with open(filepath) as f:
            content = f.read()
        data = json.loads(content)
        yield Route(
            name=data["name"],
            pub_id=data["pub_id"],
            description=data["description"],
            lines=data["lines"],
        )

    @staticmethod
    def _parent_geohashes(geohash):
        for i in range(0, len(geohash)+1):
            yield geohash[:len(geohash)-i]

    @staticmethod
    def _files_in(root_dir):
        for root, subdirs, files in os.walk(root_dir):
            for f in files:
                if f.startswith("route_"):
                    yield os.path.join(root, f)


