from haystack import indexes

from common.models import Item


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Item

    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated."""
    #     return self.get_model().objects.filter(timestamp__lte=timezone.now())

    def prepare(self, item):
        self.prepared_data = super(ItemIndex, self).prepare(item)
        self.prepared_data['name'] = item.name
        self.prepared_data['description'] = item.description