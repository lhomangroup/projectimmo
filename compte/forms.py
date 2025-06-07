from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from client.models import Client

TYPE_UTILISATEUR_CHOICES = [
    ('locataire', 'Locataire'),
    ('proprietaire', 'Propriétaire'),
    ('partenaire', 'Partenaire'),
]

class CreerUtilisateur(UserCreationForm):
    type_utilisateur = forms.ChoiceField(
        choices=TYPE_UTILISATEUR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Type d\'utilisateur'
    )

    class Meta:
        model=User
        fields=['username','email','type_utilisateur','password1','password2']


class CustomerForm(ModelForm):
	class Meta:
		model = Client
		fields = '__all__'
		exclude = ['user']