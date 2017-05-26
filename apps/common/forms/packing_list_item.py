from django import forms
from apps.common.models import PackingListItem, PackingList, Item


class PackingListItemForm(forms.Form):

    item_id = forms.IntegerField()
    packing_list_id = forms.IntegerField()
    packing_list_item_id = forms.IntegerField()

    def clean_item_id(self):
        try:
            item_id = self.cleaned_data.get('item_id')
        except Exception as e:
            raise forms.ValidationError("invalid item_id: %s" % item_id)
        if not Item.objects.filter(id=item_id).exists():
            raise forms.ValidationError("invalid item_id: %s" % item_id)
        return item_id

    def clean_packing_list_id(self):
        try:
            packing_list_id = self.cleaned_data.get('packing_list_id')
        except Exception as e:
            raise forms.ValidationError("invalid packing_list_id: %s" % packing_list_id)
        if not PackingList.objects.filter(id=packing_list_id).exists():
            raise forms.ValidationError("invalid packing_list_id: %s" % packing_list_id)
        return packing_list_id

    def clean_packing_list_item_id(self):
        try:
            packing_list_item_id = self.cleaned_data.get('packing_list_item_id')
        except Exception as e:
            raise forms.ValidationError("invalid packing_list_item_id: %s" % packing_list_item_id)
        if not PackingListItem.objects.filter(id=packing_list_item_id).exists():
            raise forms.ValidationError("invalid packing_list_item_id: %s" % packing_list_item_id)
        return packing_list_item_id