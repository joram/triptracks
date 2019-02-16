from apps.routes.stores.s3_routes import S3RoutesStore
from apps.routes.stores.cached_routes import CachedRoutesStore

ZOOM_LEVELS = {
    0: 1,
    1: 1,
    2: 1,
    3: 5,
    4: 5,
    5: 5,
    6: 10,
    7: 10,
    8: 10,
    9: 25,
    10: 25,
    11: 100,
    12: 100,
    13: 500,
    14: 500,
    15: 1000,
    16: 1000,
    17: 1500,
    18: 1500,
    19: 2000,
    20: 2000,
}


def get_cache(zoom=1):
    max_verts = ZOOM_LEVELS[zoom]
    return CachedRoutesStore(max_verts, S3RoutesStore())
