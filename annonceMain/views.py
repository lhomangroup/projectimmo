from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from account.models import *
from .models import *
from annonce.models import *
from annonce.forms import *
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from annonce.models import *
from annonce.filters import OrderFilter
from django.contrib.auth.decorators import login_required
from itertools import chain
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    """Vue principale - redirige vers annonceHome"""
    return redirect('annonceHome')

def annonceHome(request):
    query_ville = request.GET.get('query_ville')
    query_location = request.GET.get('query_location')
    query_locataires = request.GET.get('query_locataires')
    lastannonce = Annonce.objects.select_related('address').prefetch_related('imagelogement_set').all().order_by('-id')[:6]
    context = {'annonce': lastannonce}
    return render(request, 'annonce/search/annonceHome.html', context)

def searchPage(request):
    myFilter = Annonce.objects.all()
    image = ImageLogement.objects.all()
    query_ville = request.GET.get('query_ville')
    query_location = request.GET.get('query_location')
    query_locataires = request.GET.get('query_locataires')

    if query_ville != '' and query_ville is not None:
        myFilter = myFilter.filter(address__ville__icontains=query_ville)

    if query_locataires != '' and query_locataires is not None:
        myFilter = myFilter.filter(nombre_personne=query_locataires)

    if query_location != '' and query_location is not None:
        myFilter = myFilter.filter(dureeLocationMaxi=query_location)

    if query_ville != '' and query_ville is not None and query_locataires != '' and query_locataires is not None:
        myFilter = myFilter.filter(address__ville__icontains=query_ville, nombre_personne=query_locataires)

    if query_ville != '' and query_ville is not None and query_locataires != '' and query_locataires is not None and \
            query_location != '' and query_location is not None:
        myFilter = myFilter.filter(address__ville__icontains=query_ville, nombre_personne=query_locataires,
                                   dureeLocationMaxi = query_location)

    context = {'annonces': myFilter, 'image':image}
    return render(request, 'annonce/search/search_page.html', context)

def detail_annonce(request, pk):
    myObject = Annonce.objects.get(id=pk)
    image = ImageLogement.objects.all()
    categorie_service = myObject.categorie_service.all()
    services = Services.objects.all()
    context = {'annonce': myObject, 'myImages': image, 'categorie_service': categorie_service, 'services':services,
               'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY}
    return render(request, 'annonce/search/annonce_result.html', context)

class SuccessView(TemplateView):
    template_name = "annonce/search/success.html"

class CancelView(TemplateView):
    template_name = "annonce/search/cancel.html"

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Annonce.objects.get(id=product_id)
        print(product)

        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        price = self.kwargs["price"]
        print(price)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': round(price * 100),
                        'product_data': {
                            'name': product.titre_logement,
                        },
                    },
                        'quantity': 1,
                },
                ],
                metadata={
                    "product_id": product.id
                },
                mode='payment',
                success_url=YOUR_DOMAIN + 'success/',
                cancel_url=YOUR_DOMAIN + 'cancel/',
                customer_email=request.user.email,
            )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

        # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase...
        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]
        myAnnonce = Annonce.objects.get(id=product_id)
        user = Account.objects.get(email=customer_email)
        myAnnonce.reservation = user
        myAnnonce.reserved = True
        myAnnonce.save()

    # Passed signature verification
    return HttpResponse(status=200)