# from foot.views import JoueurListView
from .views import *
# from django.conf.urls import url
from django.urls import include, re_path

from django.urls import path, include
from django.urls import include, path
from rest_framework import routers
from django.views.generic.dates import ArchiveIndexView
from django.contrib.auth.decorators import login_required, permission_required

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('soumission/checkbox/', views.savevalues),

    # path('request-meeting/<pk:int>', views.invoice),
    # path('<pk:int>/', soumission.as_view(), name='valide'),
    path('client/', SoumissionCreateView.as_view(), name='soumission-add'),

    path('validation/', SoumissionSigner.as_view(), name='signer'),

    # url('soumission/validation/<int:id>/', views.validate, name='invoice-one'),
]
