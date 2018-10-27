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

            i = 0

            keys = activity_generators.keys()
            while len(keys) > 0:
                def get_results(i):
                    if len(keys) == 0:
                        return None, None, None
                    key = keys[i % len(keys)]
                    activity_generator = activity_generators[key]["generator"]
                    account = activity_generators[key]["account"]
                    try:
                        results = activity_generator.next()
                    except:
                        keys.remove(key)
                        return get_results(i)
                    activity, created = results
                    return account, activity, created

                account, activity, created = get_results(i)
                if account is None:
                    break
                i += 1
                print "got activity:{activity_name} for account:{username} created:{created}".format(
                    activity_name=activity.route.name,
                    username=account.user.get_short_name(),
                    created=created,
                )
                time.sleep(sleep_s)
        except Exception as e:
            print "error!"
            print e

        print "finished polling all accounts. sleeping for 10min"
        time.sleep(600)

#
# def start():
#     print "starting strava collection thread"
#     return thread.start_new_thread(pull_strava_activities, (5,))
#

# _COLLECT_THREAD = None
# if _COLLECT_THREAD is None:
#     _COLLECT_THREAD = start()
