from django.urls import path,include
from Authentication import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path("",views.home,name="home")
]
