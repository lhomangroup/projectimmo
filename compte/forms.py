from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm
from client.models import Client

User = get_user_model()

TYPE_UTILISATEUR_CHOICES = [
    ('locataire', 'Locataire'),
    ('proprietaire', 'Propriétaire'),
    ('partenaire', 'Partenaire'),
]

class CreerUtilisateur(UserCreationForm):
    type_utilisateur = forms.ChoiceField(choices=TYPE_UTILISATEUR_CHOICES)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'telephone', 'password1', 'password2', 'type_utilisateur']


class CustomerForm(ModelForm):
	class Meta:
		model = Client
		fields = '__all__'
		exclude = ['user']