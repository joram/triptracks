import mock
from schema import schema
from stores.routes import RoutesStore


def mock_get_cache(zoom):
  return RoutesStore()


@mock.patch('models.route.get_cache', mock_get_cache)
def test_basic_schema():
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
  print(result.to_dict())
  assert result.to_dict() == {}


@mock.patch('models.route.get_cache', mock_get_cache)
def test_trip_plans_schema():
  query = '''query {
    tripPlans{
      owner{
        profileImage
        name      
      }
      attendees {
        pubId
        profileImage
        name
      }
    }
  }'''
  result = schema.execute(query)
  print(result.to_dict())
  assert result.to_dict() == {}

