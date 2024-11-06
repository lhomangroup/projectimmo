from django.forms import ModelForm
from .models import Client
from address.forms import AddressField

class ClientForm(ModelForm):
    class Meta:
        model=Client
        fields='__all__'
