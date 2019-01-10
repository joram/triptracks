from routes.models.route import Route
from routes.stores.routes import RoutesStore
from apps.accounts.models import User
import random
import names
import mock

route_store = None

def mock_get_cache(zoom):
  global route_store
  if route_store is None:
    route_store = RoutesStore()
    route_store.dir = route_store.dir.replace("routes_store", "routes_store_test")
    route_factory = RouteFactory()
    for i in range(0, 10):
      route_store.add(route_factory.get())
  return route_store


class BaseFactory(object):

  def __init__(self, seed=123, pub_id_prefix="unknown"):
    self.random = random.Random()
    self.random.seed(seed)
    self.pub_id_prefix = pub_id_prefix
    self.generated = 0
    self.base_owner, _ = User.objects.get_or_create(email="original@owner.com", pub_id="user_route_system_owner")


  def pub_id(self):
    s = "{}_{}".format(self.pub_id_prefix, str(self.generated))
    self.generated += 1
    return s


  def name(self):
    with mock.patch("names.random", self.random):
      return names.get_full_name()


class RouteFactory(BaseFactory):

  def __init__(self):
    BaseFactory.__init__(self, 123, "route")

  def lines(self):
    return [[
      (48.4284, -123.3656, None),
      (48.4285, -123.3656, None),
      (48.4285, -123.3657, None),
    ]]

  def description(self):
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs")
    adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")
    l = [nouns, verbs, adj, adv]
    return ' '.join([self.random.choice(i) for i in l])

  def get(self):
    route = Route(
      lines=self.lines(),
      name=self.name(),
      description=self.description(),
      pub_id=self.pub_id(),
      zoom=self.random.randint(0, 20),
      owner_pub_id=self.base_owner.pub_id,
    )
    return route

