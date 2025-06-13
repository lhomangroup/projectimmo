from django.urls import path
from . import views
from .views import SoumissionCreateView, SoumissionSigner

urlpatterns = [
    path('', views.soumission_home, name='soumission-home'),
    # path('admin/', admin.site.urls),
    path('soumission/checkbox/', views.savevalues),

    # path('request-meeting/<pk:int>', views.invoice),
    # path('<pk:int>/', soumission.as_view(), name='valide'),
    path('client/', SoumissionCreateView.as_view(), name='soumission-add'),

    path('validation/', SoumissionSigner.as_view(), name='signer'),

    # url('soumission/validation/<int:id>/', views.validate, name='invoice-one'),
]