from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('annonceHome/', views.annonceHome, name='annonceHome'),
    path('searchPage/', views.searchPage, name='searchPage'),
    path('detail/<int:pk>/', views.detail_annonce, name='detail_annonce'),
]