from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='conciergerie-index'),
    path('search/', views.search_conciergerie, name='search-conciergerie'),
]