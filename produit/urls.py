from django.urls import path
from . import views

urlpatterns = [
    path('', views.annonceHome, name='annoncehome'),
    path('annonce/searchPage/', views.searchPage, name='searchPage'),
    path('annonce/detail_annonce/<str:pk>/', views.detail_annonce, name='detail_annonce'),
    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products_create/', views.products_create, name='products_create'),
    path('products_update/<str:pk>/', views.products_update, name='products_update'),
    path('products_delete/<str:pk>/', views.products_delete, name='products_delete'),
    path('create-checkout-session/<str:pk>/<int:price>/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
]