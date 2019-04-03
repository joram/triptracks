import graphene
from apps.accounts.models import User
from graphene_django.types import DjangoObjectType


class CreateUser(graphene.Mutation):
    class Arguments:
        google_credentials = graphene.JSONString()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)

    def mutate(self, info, google_credentials):
        import pprint
        profile = google_credentials.get("googleCreds", {}).get("profileObj", {})
        pprint.pprint(profile)
        # todo: validate
        user = User(google_credentials=google_credentials)
        user.save()
        ok = True
        return CreateUser(user=user, ok=ok)


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
