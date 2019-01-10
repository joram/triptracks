import json
import mock
import datetime
from routes.models.route import Route
from routes.models.test_utils import mock_get_cache
from apps.accounts.models import User
from apps.integrations.views.strava import webhooks as strava_webhook_view
from apps.integrations.models.strava import StravaAccount, StravaActivity
from stravalib.model import Activity


def mock_get_activity(self, activity_id):
  activity = mock.Mock()
  activity.id = activity_id
  activity.name = "new strava route"
  return activity


def mock_get_gpx_file(self, activity_id):
  return '''<?xml version="1.0" encoding="UTF-8"?>
<gpx
  version="1.0"
  creator="GPSBabel - http://www.gpsbabel.org"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns="http://www.topografix.com/GPX/1/0"
  xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">
<time>2009-05-20T16:06:06Z</time>
<bounds minlat="49.373629804" minlon="-123.193190442" maxlat="49.393682815" maxlon="-123.170844638"/>
<wpt lat="49.383079803" lon="-123.182053101">
  <time>2007-10-13T18:26:50Z</time>
  <name>4thLake</name>
  <cmt>4thLake</cmt>
  <desc>4thLake</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.387943784" lon="-123.180090990">
  <time>2007-10-13T18:26:50Z</time>
  <name>TriangleMeadows</name>
  <cmt>TriangleMeadows</cmt>
  <desc>TriangleMeadows</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.376950142" lon="-123.192869581">
  <time>2007-10-13T18:26:50Z</time>
  <name>Tubing</name>
  <cmt>Tubing</cmt>
  <desc>Tubing</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.386456277" lon="-123.174042143">
  <time>2007-10-13T18:26:50Z</time>
  <name>UnknownLake</name>
  <cmt>UnknownLake</cmt>
  <desc>UnknownLake</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.382819954" lon="-123.182555033">
  <time>2007-10-13T18:26:50Z</time>
  <name>Upper1Powerline</name>
  <cmt>Upper1Powerline</cmt>
  <desc>Upper1Powerline</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.382776368" lon="-123.178788011">
  <time>2007-10-13T18:26:50Z</time>
  <name>Upper2Powerline</name>
  <cmt>Upper2Powerline</cmt>
  <desc>Upper2Powerline</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.380964578" lon="-123.186872864">
  <time>2007-10-13T18:26:50Z</time>
  <name>Upper3Powerline</name>
  <cmt>Upper3Powerline</cmt>
  <desc>Upper3Powerline</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.376930445" lon="-123.186787310">
  <time>2007-10-13T18:26:50Z</time>
  <name>UpperBurfield</name>
  <cmt>UpperBurfield</cmt>
  <desc>UpperBurfield</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.379988489" lon="-123.179575588">
  <time>2007-10-13T18:26:50Z</time>
  <name>UpperMobratten</name>
  <cmt>UpperMobratten</cmt>
  <desc>UpperMobratten</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.380373617" lon="-123.185188431">
  <time>2007-10-13T18:26:50Z</time>
  <name>UpperTelemark</name>
  <cmt>UpperTelemark</cmt>
  <desc>UpperTelemark</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.383250142" lon="-123.180693845">
  <time>2007-10-13T18:26:50Z</time>
  <name>UpperWarmingHut</name>
  <cmt>UpperWarmingHut</cmt>
  <desc>UpperWarmingHut</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.380981582" lon="-123.181277953">
  <time>2007-10-13T18:26:50Z</time>
  <name>UpperWellsGrey</name>
  <cmt>UpperWellsGrey</cmt>
  <desc>UpperWellsGrey</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.373901710" lon="-123.172981191">
  <time>2007-10-13T18:26:50Z</time>
  <name>WestLakeHill</name>
  <cmt>WestLakeHill</cmt>
  <desc>WestLakeHill</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.377228298" lon="-123.172831683">
  <time>2007-10-13T18:26:50Z</time>
  <name>WestLakeTrail</name>
  <cmt>WestLakeTrail</cmt>
  <desc>WestLakeTrail</desc>
  <sym>Waypoint</sym>
</wpt>
<wpt lat="49.376001673" lon="-123.183721398">
  <time>2007-10-13T18:26:50Z</time>
  <name>ZigZag</name>
  <cmt>ZigZag</cmt>
  <desc>ZigZag</desc>
  <sym>Waypoint</sym>
</wpt>
<trk>
  <name>- From1Waypoints</name>
<trkseg>
<trkpt lat="49.377013431" lon="-123.176330091">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377024973" lon="-123.176429321">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377043627" lon="-123.176583682">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377029922" lon="-123.176722773">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377011767" lon="-123.176830162">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.376991759" lon="-123.176973363">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.376969973" lon="-123.177102781">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.376961698" lon="-123.177219849">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.376978586" lon="-123.177352162">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377006293" lon="-123.177467982">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377054711" lon="-123.177568723">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377101366" lon="-123.177646038">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377168632" lon="-123.177774399">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377219804" lon="-123.177839333">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377268220" lon="-123.177941452">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377320204" lon="-123.178062871">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377359642" lon="-123.178153937">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377419726" lon="-123.178272631">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377475342" lon="-123.178372022">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377514796" lon="-123.178452068">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377573078" lon="-123.178572133">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377619714" lon="-123.178661849">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377668134" lon="-123.178761214">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377721897" lon="-123.178895041">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377786584" lon="-123.178944871">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377858471" lon="-123.178991972">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377928504" lon="-123.179074885">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.377979675" lon="-123.179139820">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.378047924" lon="-123.179213084">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.378106295" lon="-123.179275290">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.378173663" lon="-123.179336152">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.378234697" lon="-123.179421789">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.378302947" lon="-123.179493676">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.378368517" lon="-123.179554532">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.378436767" lon="-123.179626419">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
<trkpt lat="49.378503234" lon="-123.179688656">
  <time>2007-10-13T18:26:50Z</time>
</trkpt>
</trkseg>
</trk>
</gpx>
'''


@mock.patch('apps.integrations.models.strava.StravaClient.get_gpx_file', mock_get_gpx_file)
@mock.patch('apps.integrations.models.strava.StravaClient.get_activity', mock_get_activity)
@mock.patch('apps.integrations.models.strava.get_cache', mock_get_cache)
def test_webhook_creates_route():
  user, _ = User.objects.get_or_create(email="test_strava@test.com", pub_id="user_testingstrava")
  account, _ = StravaAccount.objects.get_or_create(
    pub_id="strava_account_0",
    user_pub_id=user.pub_id,
    access_token="access_token_123",
    strava_athlete_id=0
  )
  mock_request = mock.MagicMock()
  mock_request.method = "POST"
  mock_request.body = json.dumps({
    "aspect_type": "not deleting",
    "event_time": "datetime.datetime.now()",
    "object_id": 0,
    "object_type": "activity",
    "owner_id": 0,
    "subscription_id": "",
    "updates": {}
  })

  # Act
  strava_webhook_view(mock_request)

  route = mock_get_cache(0).get_by_pub_id("route_a9109c907542e71231c1cddd830d0059")
  assert route.name == "new strava route"
  assert route.owner_pub_id == user.pub_id

  activity = StravaActivity.objects.get(strava_account_pub_id=account.pub_id)
  assert activity.route.pub_id == route.pub_id
  mock_get_cache(0).delete(route.pub_id)
