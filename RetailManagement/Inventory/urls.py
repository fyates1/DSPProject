from django.contrib import admin
from django.urls import path, include
from Inventory import views
from django.conf import settings
from django.conf.urls.static import static
app_name="Inventory"
urlpatterns = [
    path("home/",views.home,name = "home"),
    path("add_product/",views.add_product,name ="add_product"),
    path("bulkAddProducts/",views.bulk_add_products,name="bulk_add_products"),
    path("product_list/",views.product_list,name="product_list"),
    path("show_product/<product_id>",views.show_product,name="show_product"),
    path("add_product_to_store/<product_id>",views.add_product_to_store,name="add_product_to_store"),
    path("view_orders/",views.view_orders,name="view_orders"),
    path("active_products/",views.list_active_products,name="list_active_products"),
    path("addStockItem/<product_id>",views.addStockItem,name="addStockItem"),
    path("view_inventory/",views.view_inventory,name="view_inventory"),
    path("writeoff/",views.writeoff,name="writeoff"),
    path("view_writeoff/",views.view_writeOffs,name="view_writeOffs"),
    path("reSequenceProducts/",views.reSequenceProducts,name="reSequenceProducts"),
    path("placeAfter/",views.placeAfter,name="placeAfter")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
