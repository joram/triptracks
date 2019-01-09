from routes.models.route import Route
import random
import names
import uuid
import mock


class BaseFactory(object):

  def __init__(self, seed=123, pub_id_prefix="unknown"):
    self.random = random.Random()
    self.random.seed(seed)
    self.pub_id_prefix = pub_id_prefix

  def pub_id(self):
    return "{}_{}".format(self.pub_id_prefix, str(uuid.UUID(int=self.random.getrandbits(128))).replace("-", ""))


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
    )
    return route

