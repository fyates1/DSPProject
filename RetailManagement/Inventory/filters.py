import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    Category = django_filters.CharFilter(field_name="Category",lookup_expr="exact")
    ProductName = django_filters.CharFilter(field_name="ProductName", lookup_expr="icontains")
    class Meta:
        model = Product
        fields = ["Category","ProductName"]