import thread
import time
from apps.integrations.models import StravaAccount


def pull_strava_activities(sleep_s):
    while True:
        try:
            activity_generators = {}
            for account in StravaAccount.objects.all():
                activity_generators[account.pub_id] = {
                    "generator": account.populate_activities(),
                    "account": account,
                }

            for key in activity_generators:
                activity_generator = activity_generators[key]["generator"]
                account = activity_generators[key]["account"]
                results = activity_generator.next()
                if results is None:
                    print "got no results"
                    del activity_generators[key]
                    continue

                activity, created = results
                print "got activity:{activity_name} for account:{username} created:{created}".format(
                    activity_name=activity.route.name,
                    username=account.user.get_short_name(),
                    created=created,
                )
                time.sleep(sleep_s)
        except Exception as e:
            print e

        print "finished polling all accounts. sleeping for 10min"
        time.sleep(600)


def start():
    print "starting strava collection thread"
    return thread.start_new_thread(pull_strava_activities, (5,))


_COLLECT_THREAD = None
if _COLLECT_THREAD is None:
    _COLLECT_THREAD = start()
