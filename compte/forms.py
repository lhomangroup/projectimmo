from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from client.models import Client
from django import forms

from .models import *


class CreerUtilisateur(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class CustomerForm(ModelForm):
	class Meta:
		model = Client
		fields = '__all__'
		exclude = ['user']