import graphene
from apps.packing.models import PackingList, PackingListItem, Item
from graphene_django.types import DjangoObjectType


class ItemType(DjangoObjectType):
  weight = graphene.Float()

  def resolve_weight(self, info):
    return self.weight

  class Meta:
    model = Item


class PackingListType(DjangoObjectType):
  weight = graphene.Float()
  item_count = graphene.Int()
  items = graphene.List(lambda: PackingListItemType)

  def resolve_weight(self, info):
    return self.weight

  def resolve_item_count(self, info):
    return self.item_count

  def resolve_items(self, info):
    return PackingListItem.objects.filter(packing_list_pub_id=self.pub_id)

  class Meta:
    model = PackingList


class PackingListItemType(DjangoObjectType):
  item = graphene.Field(ItemType)

  def resolve_item(self, info):
    return Item.objects.get(pub_id=self.item_pub_id)

  class Meta:
    model = PackingListItem


class PackingQuery(object):
    packing_lists = graphene.List(PackingListType)
    packing_list = graphene.Field(PackingListType, pub_id=graphene.String())

    def resolve_packing_lists(self, info):
      return PackingList.objects.all()

    def resolve_packing_list(self, info, pub_id):
      return PackingList.objects.get(pub_id=pub_id)

