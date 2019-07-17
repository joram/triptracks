import graphene
from apps.accounts.models import User, SessionTokenGraphene
from graphene_django.types import DjangoObjectType
from utils.auth import get_or_create_session_token


class CreateUser(graphene.Mutation):
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
            return CreateUser(user=qs[0], ok=True, session_token=token)

        user = User(google_credentials=google_credentials)
        user.save()
        token, created = get_or_create_session_token(user)
        return CreateUser(user=user, ok=True, session_token=token)


class UserType(DjangoObjectType):
  profile_image = graphene.String()
  pub_id = graphene.String()
  name = graphene.String()

  def resolve_profile_image(self, info):
    if self.google_credentials is None:
      return None
    return self.google_credentials.get("picture")

  def resolve_name(self, info):
    print(self.google_credentials)
    if self.google_credentials is None:
      return None
    return self.google_credentials.get("name")

  class Meta:
    exclude_fields = ('password', 'email', 'googleCredentials')
    model = User
