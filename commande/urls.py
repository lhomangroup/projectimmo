from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.liste_commandes),
    path('ajout_commande/',views.ajouter_commande, name='ajout_commande'),
    path('modifie_commande/<str:pk>', views.modifier_commande, name='modifie_commande'),
    path('supprime_commande/<str:pk>', views.supprimer_commande, name='supprime_commande'),
]