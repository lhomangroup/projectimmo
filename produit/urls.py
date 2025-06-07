from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produits/', views.products, name='products'),
    path('create/', views.products_create, name='create_product'),
    path('update/<str:pk>/', views.products_update, name='update_product'),
    path('delete/<str:pk>/', views.products_delete, name='delete_product'),
]