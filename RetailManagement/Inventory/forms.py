from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from .models import Product, ActiveProduct, StockItem,WriteOff
from django.forms import ModelForm

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class CSVUploadForm(forms.Form):
    file=forms.FileField()
class ActiveItemForm(ModelForm):
    class Meta:
        model = ActiveProduct
        fields = ("minimumStockQuantity","Class")

class StockItemForm(ModelForm):
    bestBeforeDate = DateField(widget=forms.SelectDateWidget,required=False)
    class Meta:
        model = StockItem
        fields = ("bestBeforeDate","quantity")

class WriteOffForm(ModelForm):
    class Meta:
        model = WriteOff
        fields = ("quantity","reason")

class moveProductForm(forms.Form):
    Product = forms.ModelChoiceField(queryset=ActiveProduct.objects.all())
    PlaceItemAfter = forms.ModelChoiceField(queryset=ActiveProduct.objects.all())