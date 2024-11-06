from django.urls import path
from . import views


urlpatterns = [
    path('workflow', views.workflow, name='workflow'),
    path('workflow/workrep/<str:pk>', views.workrep, name='workrep'),
    path('workflow/final/<str:pk>', views.workfinal, name='final'),
]