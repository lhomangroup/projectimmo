from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>', views.liste_clients, name='client'),
    path('ajout_client/', views.ajouter_client, name='ajout_client'),
    path('update_client/<str:pk>/', views.update_client, name='update_client'),
    path('delete_client/<str:pk>/', views.delete_client, name='delete_client'),
]
