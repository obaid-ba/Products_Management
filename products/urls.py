from django.urls import path
from . import views


urlpatterns = [
    path('', views.products, name='products'),
    path('create/', views.newproduct, name='newproduct'),
    path('delete/<int:id>/', views.deleteproduct, name='deleteproduct'),
    path('edit/<int:id>/', views.editproduct, name='editproduct'),
]
