from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_view, name='blog'),
    path('create_post/', views.create_post_view, name='create_post'),
    path('post_delete/<str:id>', views.delete_post, name='post_delete'),
    path('post_update/<str:id>', views.update_post, name='post_update'),
    path('<str:id>', views.detail_view, name='detail_view'),
]