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


# Create your views here.
def home(request):
    query_ville = request.GET.get('place')
    query_location = request.GET.get('query_location')
    query_locataires = request.GET.get('query_locataires')
    lastannonce = Annonce.objects.filter(address__pays__icontains="France")
    lastannonce = lastannonce.order_by('-id')[:10]

    image = ImageLogement.objects.all()
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
from annonce.models import Annonce, ImageLogement

def index(request):
    """Vue principale de la conciergerie"""
    # Récupérer les dernières annonces avec leurs images
    annonces = Annonce.objects.select_related('address').prefetch_related('imagelogement_set').all().order_by('-id')[:6]
    
    context = {'annonce': annonces}
    return render(request, 'conciergerie/index.html', context)

def search_conciergerie(request):
    """Vue de recherche dans la conciergerie"""
    query_ville = request.GET.get('query_ville', '')
    query_type = request.GET.get('query_type', '')
    query_locataires = request.GET.get('query_locataires', '')
    
    # Base queryset
    annonces = Annonce.objects.select_related('address').prefetch_related('imagelogement_set').all()
    
    # Filtrer selon les critères
    if query_ville:
        annonces = annonces.filter(address__ville__icontains=query_ville)
    
    if query_type:
        annonces = annonces.filter(type_location_choices=query_type)
    
    if query_locataires:
        annonces = annonces.filter(nombre_personne__gte=int(query_locataires))
    
    context = {
        'annonces': annonces.order_by('-id'),
        'query_ville': query_ville,
        'query_type': query_type,
        'query_locataires': query_locataires,
    }
    return render(request, 'conciergerie/search_conciergerie.html', context)