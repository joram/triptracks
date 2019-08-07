import graphene
from apps.accounts.models import User, SessionTokenGraphene
from apps.accounts.schema import UserType
from utils.auth import get_or_create_session_token


class GetOrCreateUser(graphene.Mutation):
    class Arguments:
        google_credentials = graphene.JSONString()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)
    session_token = graphene.Field(lambda: SessionTokenGraphene)

    def mutate(self, info, google_credentials):
        profile = google_credentials.get("googleCreds", {}).get("profileObj", {})
        qs = User.objects.filter(email=profile["email"])
        if qs.exists():
            user = qs[0]
            token, created = get_or_create_session_token(user)
            return GetOrCreateUser(user=qs[0], ok=True, session_token=token)

        user = User(google_credentials=google_credentials)
        user.save()
        token, created = get_or_create_session_token(user)
        return GetOrCreateUser(user=user, ok=True, session_token=token)

