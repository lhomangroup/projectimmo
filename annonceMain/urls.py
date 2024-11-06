from django.urls import path

from annonceMain import views

urlpatterns = [
    path('annonce/annonceHome/', views.annonceHome, name='annonce_home'),
    path('annonce/searchPage/', views.searchPage, name='search_annonce'),
    path('annonce/detail_annonce/<str:pk>', views.detail_annonce, name='detail_annonce'),
]