import graphene
from utils.auth import get_authenticated_user
from django.conf import settings
from apps.integrations.models import StravaAccount
from stravalib import Client
import datetime

client = Client()


class ConnectToStrava(graphene.Mutation):
    class Arguments:
        code = graphene.String()

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, code):
        user = get_authenticated_user(info)
        if user is None:
            return ConnectToStrava(ok=False, message="unauthed")

        resp = client.exchange_code_for_token(
            client_id=settings.STRAVA_CLIENT_ID,
            client_secret=settings.STRAVA_CLIENT_SECRET,
            code=code,
        )

        qs = StravaAccount.objects.filter(user_pub_id=user.pub_id)
        if qs.exists():
            strava_account = qs[0]
        else:
            strava_account = StravaAccount()
            strava_account.strava_account_id = strava_account.get_client().get_athlete().id

        strava_account.access_token = resp["access_token"]
        strava_account.refresh_token = resp["refresh_token"]
        strava_account.expires_at = datetime.datetime.fromtimestamp(resp["expires_at"])
        strava_account.save()

        import pprint
        pprint.pprint(vars(strava_account))
        return ConnectToStrava(ok=True, message="created" if qs.exists() else "new")
