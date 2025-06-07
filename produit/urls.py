from django.urls import path
from . import views

urlpatterns = [
    path('', views.annonceHome, name='acceuil'),
    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/create/', views.products_create, name='products_create'),
    path('products/update/<str:pk>/', views.products_update, name='products_update'),
    path('products/delete/<str:pk>/', views.products_delete, name='products_delete'),
]