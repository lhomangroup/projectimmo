from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ClientForm
from .models import Client
from commande.filtres import CommandeFiltre

# from .models import memory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='acces')
def liste_clients(request,pk):
    client=Client.objects.get(id=pk)
    commande=client.commande_set.all()
    commande_total = commande.count()
    # myFilter=CommandeFiltre(request.GET,queryset=commande)
    myFilter = CommandeFiltre(request.GET,queryset=commande)
    commande=myFilter.qs
    context={'client':client,'commande':commande,'commande_total':commande_total,'myFilter':myFilter}
  #  context={'client':client,'commande':commande}
    return render(request,'client/liste_clients.html',context)

@login_required(login_url='acces')
def ajouter_client(request):
    form=ClientForm()
    if request.method=='POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ClientForm()

    context = {'form': form}

    return render(request,'client/ajouter_client.html',context)
def update_client(request, pk):

    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)
    if request.method=='POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ClientForm(instance=client)
    context = {'form': form}
    return render(request,'client/ajouter_client.html',context)

def delete_client(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == "POST":
        client.delete()
        return redirect('/')
    context = {'client': client}
    return render(request, 'client/suppr_client.html', context)