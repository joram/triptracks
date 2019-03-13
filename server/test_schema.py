import django
django.setup()

import pprint
import mock
from schema import schema
from apps.routes.models.test_utils import mock_get_cache
from collections import OrderedDict
from apps.trips.models import Plan, TripAttendee
from apps.accounts.models import User
from apps.packing.models import PackingList, PackingListItem, Item


@mock.patch('schema.get_cache', mock_get_cache)
def test_single_route():

  query = '''
    query {
      route(pubId:"route_0"){
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
          OrderedDict([('pubId', 'route_0'),
             ('name', 'Christopher Dryer'),
             ('lines',
              '[[[48.4284, -123.3656, null], '
              '[48.4285, -123.3656, null], '
              '[48.4285, -123.3657, null]]]'),
             ('owner',
              OrderedDict([('pubId', None),
                 ('profileImage',
                  None)]))]))]))])
  pprint.pprint(result.to_dict())
  assert result.to_dict() == expected


@mock.patch('schema.get_cache', mock_get_cache)
def test_multiple_routes():
  query = '''
    query {
      routes(geohash:"", zoom:10){
        pubId
        name
        lines
        geohash
      }
    }
  '''
  
  result = schema.execute(query)

  expected = OrderedDict([('data',
              OrderedDict([('routes',
                            [OrderedDict([('pubId', 'route_9'),
                                          ('name', 'Harry Custodio'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_3'),
                                          ('name', 'Misty Lee'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_2'),
                                          ('name', 'James Morse'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_8'),
                                          ('name', 'Hazel Mcclurkin'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_5'),
                                          ('name', 'Kimberly Mccrary'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_4'),
                                          ('name', 'Bobby Comer'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_1'),
                                          ('name', 'Heather Wilson'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_7'),
                                          ('name', 'Clayton Arteaga'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_0'),
                                          ('name', 'Christopher Dryer'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')]),
                             OrderedDict([('pubId', 'route_6'),
                                          ('name', 'Marcia Prieto'),
                                          ('lines',
                                           '[[[48.4284, -123.3656, null], '
                                           '[48.4285, -123.3656, null], '
                                           '[48.4285, -123.3657, null]]]'),
                                          ('geohash', 'c28788pg')])])]))])
  pprint.pprint(result.to_dict())
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
  pprint.pprint(result.to_dict())
  assert result.to_dict() == expected


@mock.patch('schema.get_cache', mock_get_cache)
def test_packing_list():
  item, _ = Item.objects.get_or_create(
    pub_id="item_0",
    name="an object",
    description="something generic",
    price=6.66,
  )
  packing_list, _ = PackingList.objects.get_or_create(
    pub_id="packing_list_0",
    name="a test packing list",
  )
  PackingListItem.objects.get_or_create(
    packing_list_pub_id=packing_list.pub_id,
    item_pub_id=item.pub_id,
  )
  user, _ = User.objects.get_or_create(
    email="test3@test.com",
    pub_id="user_testtesttest")
  plan, _ = Plan.objects.get_or_create(
    user_pub_id=user.pub_id,
    pub_id="plan_testtesttest3",
    packing_list_pub_id=packing_list.pub_id)

  query = '''query {
    tripPlan(pubId:"plan_testtesttest3"){
      pubId
      name
      attendees {
        name
        pubId
      }
      packingList {
        pubId
        name
        items {
          quantity
          item {
            name
            weight
          }
        }
      }
    }
  }'''

  result = schema.execute(query)

  expected = OrderedDict([('data',
      OrderedDict([('tripPlan',
          OrderedDict([('pubId', 'plan_testtesttest3'),
             ('name', ''),
             ('attendees',
              [OrderedDict([('name', None),
                            ('pubId',
                             'user_testtesttest')]),
               OrderedDict([('name', None),
                            ('pubId',
                             'user_testtesttest')])]),
             ('packingList',
              OrderedDict([('pubId',
                            'packing_list_0'),
                           ('name',
                            'a test packing list'),
                           ('items',
                            [OrderedDict([('quantity',
                                 1),
                                ('item',
                                 OrderedDict([('name',
                                               'an '
                                               'object'),
                                              ('weight',
                                               0.0)]))])])]))]))]))])
  pprint.pprint(dict(result.to_dict()))
  assert result.to_dict() == expected
