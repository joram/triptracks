import django
django.setup()

import mock
from schema import schema
from routes.stores.routes import RoutesStore
from routes.models.test_utils import RouteFactory
from collections import OrderedDict
from apps.trips.models import Plan, TripAttendee
from apps.accounts.models import User

route_store = RoutesStore()
route_store.dir = route_store.dir.replace("routes_store", "routes_store_test")
route_factory = RouteFactory()
for i in range(0,10):
  route_store.add(route_factory.get())


def mock_get_cache(zoom):
  return route_store


@mock.patch('schema.get_cache', mock_get_cache)
def test_single_route():

  query = '''
    query {
      route(pubId:"route_573e8d77550ae8898ff41e8d8944897c"){
        pubId
        name
        lines
        owner{
          pubId
          profileImage
        }
      }
    }
  '''

  result = schema.execute(query)

  expected = OrderedDict([('data',
      OrderedDict([('route',
          [OrderedDict([('pubId',
               'route_573e8d77550ae8898ff41e8d8944897c'),
              ('name', 'Christopher Dryer'),
              ('lines',
               '[[[48.4284, -123.3656, null], '
               '[48.4285, -123.3656, null], '
               '[48.4285, -123.3657, null]]]'),
              ('owner',
               OrderedDict([('pubId', None),
                    ('profileImage',
                     None)]))])])]))])
  assert result.to_dict() == expected


@mock.patch('schema.get_cache', mock_get_cache)
def test_multiple_routes():
  query = '''
    query {
      routes(geohash:"", zoom:10){
        pubId
        name
        lines
      }
    }
  '''
  
  result = schema.execute(query)

  expected = OrderedDict([('data',
    OrderedDict([('routes',
      [OrderedDict([('pubId',
                     'route_e9e4b2dd1525e9d3d1f7fbe4b9cfda65'),
                    ('name', 'Charles Dickerson'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_c4ef7978e497cd2f65f2ef7603365a08'),
                    ('name', 'Nancy Christou'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_b8654db2a147123ac3a1cbbdf6cc94e5'),
                    ('name', 'Sharika Grimes'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_e6b4f832d6a82a951b923e0a443cdef3'),
                    ('name', 'Martha Whetzel'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_573e8d77550ae8898ff41e8d8944897c'),
                    ('name', 'Christopher Dryer'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_1a1f141b72c53633bb66ecb350c1eb44'),
                    ('name', 'Frankie Arthur'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_8de04a9e5640230e55bc0a692b8d6f81'),
                    ('name', 'Wendy Cunniff'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_28dfa2980d496d4bda22594f573e8d77'),
                    ('name', 'Eddie Zanes'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_d23ee3c934f4f0407ba35975cd2ee163'),
                    ('name', 'Valerie Carroll'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_74d2b828227d82190299536a0b4c1837'),
                    ('name', 'Cicely Stewart'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_82a45999100720f69e1a06ce1bce9331'),
                    ('name', 'Thomas Newton'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_98fc4743e0edeaf1166dd683c609dcba'),
                    ('name', 'Michael Sierra'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_8546a1a97c73708cd560f64be3dd7ffa'),
                    ('name', 'Leonard Lynch'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_7ba35975cd2ee163858c2e6e57ed22d0'),
                    ('name', 'Irving Parker'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_056fb885e81775f3ca4225f72051e671'),
                    ('name', 'James Grow'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_5d0f5781a0d96aded4e3fda5169179e2'),
                    ('name', 'Joel Underwood'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_92cadf506e3e43c2e94129954ab38105'),
                    ('name', 'Steven Barnett'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_6fafc520e7e96d54006d7b3429ed479c'),
                    ('name', 'Christine Holthaus'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, null]]]')]),
       OrderedDict([('pubId',
                     'route_12c32f37e2485bb664253e838de04a9e'),
                    ('name', 'Kirk Krasner'),
                    ('lines',
                     '[[[48.4284, -123.3656, null], '
                     '[48.4285, -123.3656, null], '
                     '[48.4285, -123.3657, '
                     'null]]]')])])]))])
  assert result.to_dict() == expected


@mock.patch('schema.get_cache', mock_get_cache)
def test_trip_plans():
  user = User.objects.create(email="test@test.com", pub_id="user_testtesttest")
  user2 = User.objects.create(email="test2@test.com", pub_id="user_testtesttest2")
  plan = Plan.objects.create(user_pub_id=user.pub_id, pub_id="plan_testtesttest")
  TripAttendee.objects.create(plan_pub_id=plan.pub_id, user_pub_id=user2.pub_id)
  query = '''query {
    tripPlans{
      pubId
      owner{
        pubId
        profileImage
      }
      attendees {
        pubId
        profileImage
      }
    }
  }'''

  result = schema.execute(query)

  expected = OrderedDict([('data',
      OrderedDict([('tripPlans',
          [OrderedDict([('pubId', 'plan_testtesttest'),
              ('owner',
               OrderedDict([('pubId',
                   'user_testtesttest'),
                  ('profileImage',
                   None)])),
              ('attendees',
               [OrderedDict([('pubId',
                    'user_testtesttest'),
                   ('profileImage',
                    None)]),
                OrderedDict([('pubId',
                    'user_testtesttest2'),
                   ('profileImage',
                    None)])])]
               )]
          )]
      ))
  ])
  assert result.to_dict() == expected

