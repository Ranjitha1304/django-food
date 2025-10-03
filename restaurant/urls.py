from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant/<int:restaurant_id>/menu/', views.menu, name='menu'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
