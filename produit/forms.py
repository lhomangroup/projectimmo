from django.forms import ModelForm
from .models import Produit
from address.forms import AddressField

class ProductForm(ModelForm):
    class Meta:
        model=Produit
        fields='__all__'

