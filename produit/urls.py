from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('',views.home, name='acceuil'),
  path('produits/', views.products, name='produit'),
  path('produits/produit_create', views.products_create, name='creer_produit'),
  path('update_produit/<str:pk>/', views.products_update, name='update_produit'),
  path('delete_produit/<str:pk>/', views.products_delete, name='delete_produit'),

]
