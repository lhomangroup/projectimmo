
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.inscriptionPage, name='compte_register'),
    path('login/', views.accesPage, name='acces'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user'),
    path('settings/', views.accountSettings, name='account_settings'),
]
