from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('conciergerie/', views.home, name='conciergerie'),
    path('conciergerie/search_conciergerie' ,views.search_conciergerie, name='search_conciergerie'),
]

