from django.shortcuts import render, redirect
from .models import *
from annonce.models import *
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from annonce.models import *
from annonce.filters import OrderFilter
from django.contrib.auth.decorators import login_required
from itertools import chain
from datapackage import Package


# Create your views here.
def home(request):
    query_ville = request.GET.get('place')
    query_location = request.GET.get('query_location')
    query_locataires = request.GET.get('query_locataires')
    lastannonce = Annonce.objects.filter(address__pays__icontains="France")
    lastannonce = lastannonce.order_by('-id')[:10]

    image = ImageLogement.objects.all()
    package = Package('https://datahub.io/JohnSnowLabs/country-and-continent-codes-list/datapackage.json')
    print(package.resource_names)
    context = {'annonce': lastannonce, 'image': image}
    return render(request, 'conciergerie/index.html', context)


def search_conciergerie(request):
    myFilter = Annonce.objects.all()
    image = ImageLogement.objects.all()
    query_ville = request.GET.get('query_ville')
    query_location = request.GET.get('query_location')
    query_locataires = request.GET.get('query_locataires')
    query_place = request.GET.get('query_place')

    if query_ville != '' and query_ville is not None:
        myFilter = myFilter.filter(address__ville__icontains=query_ville, pieces_couchage=query_place)

    if query_locataires != '' and query_locataires is not None:
        myFilter = myFilter.filter(nombre_personne=query_locataires, pieces_couchage=query_place)

    if query_location != '' and query_location is not None:
        myFilter = myFilter.filter(dureeLocationMaxi=query_location, pieces_couchage=query_place)

    if query_ville != '' and query_ville is not None and query_locataires != '' and query_locataires is not None:
        myFilter = myFilter.filter(address__ville__icontains=query_ville, nombre_personne=query_locataires,
                                   pieces_couchage=query_place)

    if query_ville != '' and query_ville is not None and query_locataires != '' and query_locataires is not None and \
            query_location != '' and query_location is not None:
        myFilter = myFilter.filter(address__ville__icontains=query_ville, nombre_personne=query_locataires,
                                   dureeLocationMaxi=query_location, pieces_couchage=query_place)
    context = {'image': image, 'annonces': myFilter}
    return render(request, 'conciergerie/search_conciergerie.html', context)


from django.shortcuts import render

# Create your views here.
