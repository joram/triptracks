import graphene
from apps.accounts.models import User
from graphene_django.types import DjangoObjectType


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
