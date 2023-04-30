from django.contrib import admin
from .models import Product, StockItem, WriteOff
# Register your models here.
admin.site.register(Product)
admin.site.register(StockItem)
admin.site.register(WriteOff)