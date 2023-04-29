from django.contrib import admin
from django.urls import path, include
from Reports import views
from django.conf import settings
from django.conf.urls.static import static
app_name="Reports"
urlpatterns = [
    path("",views.home,name = "home"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
