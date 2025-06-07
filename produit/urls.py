
from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='produit'),
    path('create/', views.products_create, name='create_product'),
    path('update/<int:pk>/', views.products_update, name='update_product'),
    path('delete/<int:pk>/', views.products_delete, name='delete_product'),
]
