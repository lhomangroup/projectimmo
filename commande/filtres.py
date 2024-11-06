import django_filters
from django_filters import DateFilter

from .models import *

class CommandeFiltre(django_filters.FilterSet):
    class Meta:
        model=Commande
        fields='__all__'
        exclude=['client', 'date_creation']