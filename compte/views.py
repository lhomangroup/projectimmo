from django.shortcuts import render, redirect
from commande.models import Commande
from client.models import Client
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreerUtilisateur
from .forms import CustomerForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from client.views import liste_clients
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users, admin_only


# Create your views here.
@unauthenticated_user
def inscriptionPage(request):
    form=CreerUtilisateur()
    if request.method=='POST':
        form=CreerUtilisateur(request.POST)
        if form.is_valid():
                user=form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Client.objects.create(
                    user=user,
                    nom=user.username,
                )
                messages.success(request,'compte cree avec succes pour '+username)
                return redirect('acces')
    context={'form':form}
    return render(request,'compte/inscription.html',context)

@unauthenticated_user
def accesPage(request):
    return render(request, 'index.html')

def logoutUser(request):
    logout(request)
    return redirect('acces')


# Create your views here.
@login_required(login_url='acces')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    commandes=request.user.client.commande_set.all()
    print(commandes)
    commande_total = commandes.count()
    commande_livre = commandes.filter(status='Livre').count()
    commande_en_cours = commandes.filter(status='En instance').count()
    context = {'commandes': commandes,
               'commande_total': commande_total,
               'commande_livre': commande_livre,
               'commande_en_cours': commande_en_cours
               }
    return render(request,'user.html',context)

@login_required(login_url='acces')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	client = request.user.client
	form = CustomerForm(instance=client)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=client)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'account/account_settings.html', context)
