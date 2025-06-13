from django.urls import path
from . import views


urlpatterns = [
    path('', views.workflow, name='workflow'),
    path('workrep/<str:pk>/', views.workrep, name='workrep'),
    path('final/<str:pk>/', views.workfinal, name='final'),
]