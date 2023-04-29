from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from Inventory.models import Product, ActiveProduct, StockItem,WriteOff
from django.forms import ModelForm


class BBDForm(forms.Form):
    bestBeforeDate = DateField(widget=forms.SelectDateWidget,required=False)