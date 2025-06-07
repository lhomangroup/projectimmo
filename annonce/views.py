from pyexpat.errors import messages

from django.shortcuts import render, redirect
from django.utils.baseconv import base64
from django.views import View

from .models import Annonce
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from workflow.models import *
from workflow.forms import *

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

from .decorators import unauthenticated_user
from .forms import *
from account.models import Address
from django.contrib.auth.decorators import login_required
# Create your views here.
from projectimmo.settings import CLIENT_AUTH_ID, CLIENT_SECRET_KEY


def user_created(model, request):
    obj = model.objects.latest('id')
    if obj.user is None:
        obj.user = request.user
    obj.save()

@unauthenticated_user
def create_annonce(request):

    form = AnnonceForm()
    userForm = CreateUserForm()
    rue = request.POST.get('rue')
    voie = request.POST.get('voie')
    ville = request.POST.get('ville')
    region = request.POST.get('region')
    zip = request.POST.get('zip')
    pays = request.POST.get('pays')

    if request.method == 'POST':
        userForm = CreateUserForm(request.POST)
        annonceForm = AnnonceForm(request.POST)

        # - validate both forms
        if userForm.is_valid() and annonceForm.is_valid():
            user = userForm.save()
            email = userForm.cleaned_data['email']
            annonce = annonceForm.save()
            myAdress = AdressAnnonce.objects.create(rue=rue,voie=voie,ville=ville,region=region,zipCode=zip,pays=pays)
            myAdress.save()
            # - associate new objects with newly created user to use in dashboard
            lastAnnonce = Annonce.objects.latest('id')
            lastAnnonce.user = user
            lastAnnonce.save()
            Condition.objects.create(
                annonce=annonce,
            )
            Address.objects.create(
                account=user,
            )
            userForm.save()
            # path to view
                # - getting domain
                # - relative url to verif
                # - encode uid for security
                # - token
            uidb64=urlsafe_base64_encode(force_bytes(user.id))

            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                            'uidb64':uidb64, 'token':token_generator.make_token(user)})

            activate_url = 'http://'+domain+link
            email_subject = 'Activez votre compte'
            email_body = 'Hi '+user.first_name + ' Cliquez sur ce lien pour vérifier votre compte\n' \
                         + activate_url

            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@lhoman.com',
                [email],
            )
            email.send(fail_silently=False)
            return HttpResponse('Activez votre compte avec le lien envoyé à votre adresse mail')
    else:
        userForm = CreateUserForm()
        annonceForm = AnnonceForm()

    context = {'annonceForm': annonceForm, 'userForm': userForm}

    return render(request,'annonce/creer-annonce.html',context)

class VerificationView(View):
    def get(self, request, uidb64, token):
        userId = urlsafe_base64_decode(uidb64)
        user = Account.objects.get(id=userId)
        user.is_active = True
        user.save()
        context = {'user': user}
        return redirect('creer-annonce')

@unauthenticated_user
def inscriptionPage(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
                user=form.save()

                return redirect('acces')
    context={'form':form}
    return render(request,'compte/inscription.html',context)

@unauthenticated_user
def login_user(request):
    from django.views.decorators.csrf import csrf_protect

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('logged-annonce')

    context = {}
    return render(request, 'compte/login-annonce.html')

def logout_annonce(request):
    logout(request)
    return redirect('creer-annonce')

@login_required(login_url='login-annonce')
def logged_annonce(request):
    if request.method == 'POST':
        print(f"POST reçu pour l'utilisateur: {request.user.email}")
        print(f"Données POST: {request.POST}")
        
        annonceForm = AnnonceForm(request.POST)
        rue = request.POST.get('rue')
        voie = request.POST.get('voie')
        ville = request.POST.get('ville')
        region = request.POST.get('region')
        zip = request.POST.get('zip')
        pays = request.POST.get('pays')

        print(f"Form valide: {annonceForm.is_valid()}")
        if annonceForm.is_valid():
            # Import nécessaire pour AdressAnnonce
            from annonce.models import AdressAnnonce, Condition
            
            print("Création de l'adresse...")
            # Créer l'adresse
            myAdress = AdressAnnonce.objects.create(
                rue=rue or '',
                voie=voie or '', 
                ville=ville or '',
                region=region or '',
                zipCode=zip or '',
                pays=pays or 'France'
            )
            print(f"Adresse créée: ID {myAdress.id}")
            
            print("Création de l'annonce...")
            # Créer l'annonce
            annonce = annonceForm.save(commit=False)
            annonce.user = request.user
            annonce.address = myAdress
            annonce.save()
            print(f"Annonce créée: ID {annonce.id} pour l'utilisateur {annonce.user.email}")
            
            # Créer une condition pour cette annonce
            print("Création de la condition...")
            Condition.objects.create(annonce=annonce)
            print("Condition créée avec succès")
            
            return redirect(reverse('dashboard-annonce', kwargs={'pk': annonce.id}))
        else:
            # Afficher les erreurs du formulaire pour debug
            print("Erreurs du formulaire:", annonceForm.errors)
            print("Données POST reçues:", request.POST)
    else:
        annonceForm = AnnonceForm()

    context = {'annonceForm': annonceForm}
    return render(request, 'annonce/logged-annonce.html', context)

@login_required
def dashboard_view(request, pk):
    myObject = Annonce.objects.get(id=pk)
    context = {'obj': myObject}
    return render(request, 'annonce/dashboard/dashboard.html', context)

@login_required
def gerer_annonce(request):
    requete = request.user
    myObject = Annonce.objects.filter(user=request.user)
    context = {'obj': myObject}
    return render(request, 'annonce/dashboard/gerer-annonce.html', context)

@login_required
def dashboard_list(request):
    """Vue principale du tableau de bord listant toutes les annonces de l'utilisateur"""
    annonces = Annonce.objects.filter(user=request.user).order_by('-id')
    context = {'annonces': annonces}
    return render(request, 'annonce/dashboard/dashboard_list.html', context)

@login_required
def description_view(request, pk):
    form = DescriptionForm()
    myObject = Annonce.objects.get(id=pk)
    requete = request.user
    rue = request.POST.get('rue')
    voie = request.POST.get('voie')
    ville = request.POST.get('ville')
    region = request.POST.get('region')
    zip = request.POST.get('zip')
    pays = request.POST.get('pays')
    address = request.POST.get('adressComplete')
    myAdress = myObject.address
    if request.method == 'POST':
        form = DescriptionForm(request.POST, instance=myObject)
        if form.is_valid():
            if address == '':
                form.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                myAdress.rue = rue
                myAdress.voie = voie
                myAdress.ville = ville
                myAdress.region = region
                myAdress.zipCode = zip
                myAdress.pays = pays
                myAdress.save()
                user = form.save()
                form.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    if request.method =='POST':
        form = DescriptionForm(request.POST, instance=myObject)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = DescriptionForm(instance=myObject)
    context = {'form': form, 'obj': myObject, 'requete': requete, 'address': myAdress}
    return render(request,'annonce/dashboard/description.html',context)

@login_required
def equipment_view(request, pk):
    form = EquipmentForm()
    requete = request.user
    myObject = Annonce.objects.get(id=pk)
    services = CategorieServicesForm()
    categories = CategorieService.objects.all()
    if request.method =='POST':
        form = EquipmentForm(request.POST, instance=myObject)
        categorie_service = request.POST.getlist('categorie_service')
        length = len(categorie_service)
        for thisCategorie in categories:
            if thisCategorie.nom in categorie_service:
                myObject.categorie_service.add(thisCategorie)
            elif thisCategorie.nom not in categorie_service:
                myObject.categorie_service.remove(thisCategorie)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = EquipmentForm(instance=myObject)
    context = {'form': form, 'requete': requete, 'obj': myObject, 'services': services}
    return render(request,'annonce/dashboard/equipements.html',context)

@login_required
def dureeLocation_view(request, pk):
    # - getting value from the displayed select in template to update object
    dureeMaxi = request.POST.get('selectMax')
    dureeMini = request.POST.get('minSelect')
    requete = request.user
    myObject = Annonce.objects.get(id=pk)
    if request.method =='POST':
        myObject.dureeLocationMini = dureeMini
        myObject.save()
        myObject.dureeLocationMaxi = dureeMaxi
        myObject.save()

    context = {'requete': requete, 'obj': myObject}
    return render(request,'annonce/dashboard/dureeLocation.html',context)

@login_required
def loyer_view(request, pk):
    allCharges = Charges.objects.all()
    form = FormLoyer()

    requete = request.user
    myObject = Annonce.objects.get(id=pk)
    if request.method =='POST':
        form = FormLoyer(request.POST, instance=myObject)
        if form.is_valid():
            # veryfing if selected charges are in created charges objects, if so adding these charges
            # to the annonce
            for thisCharge in allCharges:
                valueCharges = request.POST.get('' + thisCharge.nom)
                if thisCharge.nom == valueCharges:
                    myObject.charges.add(thisCharge)
                else:
                    myObject.charges.remove(thisCharge)
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            form = FormLoyer(instance=myObject)


    context = {'requete': requete, 'obj': myObject, 'charges': allCharges, 'form': form}
    return render(request,'annonce/dashboard/loyer.html',context)

@login_required
def image_view(request, pk):
    myObject = Annonce.objects.get(id=pk)
    myImages = ImageLogement.objects.filter(annonce=myObject)
    if request.method == 'POST':
        length = request.POST.get('length')
        # managing multi image selection with filepond
        for file_num in range(0, int(length)):
            ImageLogement.objects.create(
                annonce=myObject,
                images=request.FILES.get(f'images{file_num}')
             )

    context = {'obj': myObject, 'images': myImages}
    return render(request,'annonce/dashboard/photos.html',context)


def delete_image(request, pk):
    deletedImage = ImageLogement.objects.get(id=pk)
    thisId = deletedImage.annonce.id
    deletedImage.delete()
    return HttpResponseRedirect(reverse("dashboard-image", args=[thisId]))

@login_required
def calendrier(request, pk):
    myObject = Annonce.objects.get(id=pk)
    calendriers = Calendrier.objects.filter(annonce=myObject)
    context={'obj':myObject, 'calendrier': calendriers}
    return render(request,'annonce/dashboard/calendrier.html',context)

@login_required
def create_calendrier(request,pk):
    annonce = Annonce.objects.get(id=pk)
    debut = request.POST.get('calendrier_debut')
    fin = request.POST.get('calendrier_fin')
    disponibilite = request.POST.get('disponibilite')
    if request.method=='POST':
        calendrier = Calendrier.objects.create(
            annonce=annonce,
            calendrier_debut=debut,
            calendrier_fin=fin,
            disponibilite=disponibilite,
        )
        calendrier.save()
        return HttpResponseRedirect(reverse("dashboard-calendrier", args=[annonce.id]))
    context = {'annonce' : annonce}
    return render(request,'annonce/dashboard/create-calendrier.html',context)

@login_required
def edit_calendrier(request, pk):
    calendrier = Calendrier.objects.get(id=pk)
    annonce = calendrier.annonce
    debut = request.POST.get('calendrier_debut')
    fin = request.POST.get('calendrier_fin')
    disponibilite = request.POST.get('disponibilite')
    if request.method == 'POST':
        calendrier.calendrier_debut = debut
        calendrier.calendrier_fin = fin
        calendrier.disponibilite = disponibilite
        calendrier.annonce = annonce
        calendrier.save()
        return HttpResponseRedirect(reverse("dashboard-calendrier", args=[annonce.id]))
    context = {'annonce': annonce, 'calendrier': calendrier}
    return render(request, 'annonce/dashboard/edit-calendrier.html', context)

@login_required
def delete_calendrier(request, pk):
    calendrier = Calendrier.objects.get(id=pk)
    annonce = calendrier.annonce
    context = {'annonce': annonce, 'calendrier': calendrier}
    return render(request, 'annonce/dashboard/delete-calendrier.html', context)

def delete_calendrier_confirm(request, pk):
    calendrier = Calendrier.objects.get(id=pk)
    calendrier.delete()
    context = {'calendrier': calendrier}
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required
def condition_view(request, pk):
    form = FormCondition()
    requete = request.user
    myObject = Annonce.objects.get(id=pk)
    myCondition = Condition.objects.get(annonce=myObject)
    if request.method =='POST':
        form = FormCondition(request.POST, instance=myCondition)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = FormCondition(instance=myCondition)
    context = {'form': form, 'obj': myObject, 'requete': requete}
    return render(request,'annonce/dashboard/conditions.html',context)

def diagnsotic_view(request, pk):
    form = FormDiagnostic()
    requete = request.user
    myObject = Annonce.objects.get(id=pk)
    myDiagnostic = Diagnostic.objects.get(annonce=myObject)
    if request.method =='POST':
        form = FormDiagnostic(request.POST, instance=myDiagnostic)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = FormDiagnostic(instance=myDiagnostic)
    context = {'form': form, 'obj': myObject, 'requete': requete}
    return render(request,'annonce/dashboard/diagnostic.html',context)

@login_required()
def user_view_dashboard(request, pk):

    myObject = Annonce.objects.get(id=pk)
    user = request.user
    form = UserModif(instance=user)
    rue = request.POST.get('rue')
    voie = request.POST.get('voie')
    ville = request.POST.get('ville')
    region = request.POST.get('region')
    zip = request.POST.get('zip')
    pays = request.POST.get('pays')
    myAdress = Address.objects.get(account=user)
    address = request.POST.get('adressComplete')

    if request.method == 'POST':
        form = UserModif(request.POST, instance=user)
        if form.is_valid():
            if address == '':
                form.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                myAdress.rue = rue
                myAdress.voie = voie
                myAdress.ville = ville
                myAdress.region = region
                myAdress.zipCode = zip
                myAdress.pays = pays
                myAdress.save()
                user = form.save()
                form.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = UserModif(instance=user)

    context = {'form': form, 'obj': myObject, 'address': myAdress}

    return render(request,'annonce/dashboard/userDashboard.html',context)

def verification_view(request, pk):
    myObject = Annonce.objects.get(id=pk)
    user = request.user
    form = VerifImage(instance=user)
    if request.method =='POST':
        form = VerifImage(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = VerifImage(instance=user)
    context = {'form': form, 'obj': myObject, 'user': user,}

    return render(request,'annonce/dashboard/verif.html',context)

def get_access_code(request):

    base_url = "https://account-d.docusign.com/oauth/auth"
    auth_url = "{0}response_type=code&scope=signature&client_id={1}&redirect_uri={2}".format(base_url,
                CLIENT_AUTH_ID, request.build_absolute_uri(reverse('auth_login')))

    return HttpResponseRedirect(auth_url)

def auth_login(request):

    base_url = 'https://account-d.docusign.com/oauth/token'
    auth_code_string = '{0}:{1}'.format(CLIENT_AUTH_ID, CLIENT_SECRET_KEY)
    auth_token = base64.b64encode(auth_code_string.encode())

    req_headers = {"Authorization": "Basic {0}".format(auth_token.decode('utf-8'))}
    post_data = {'grant_type': 'authorization_code', 'code': request.GET.get('code')}

    r = request.post(base_url, data=post_data, headers=req_headers)

    response = r.json()
    return HttpResponse(response['access_token'])

    if not 'error' in response:
        return HttpResponseRedirect("{0}?token={1}".format(reverse('get_signing_url'), reponse['access_token']))
    return HttpResponse(response['error'])

def embeded_signing_ceremony(request):
    signer_email = 'hamza.aboudou@gmail.com'
    signer_name = 'Aboudou Hamza'

def profile_annonce(request):
    reservations = Annonce.objects.get(reservation=request.user)
    workflow = File.objects.get(user=request.user)
    form = NewFile(instance=workflow)
    annonce = Annonce.objects.filter(user=request.user)
    myAdress = Address.objects.get(account=request.user)
    if request.method == 'POST':
        bilan_semaine = request.POST.getlist('commentaire_bilan')
        date_bilan = request.POST.getlist('bilan_semaine')
        length = len(bilan_semaine)
        for i in range(length):
            bilan = Bilan.objects.create(commentaire=bilan_semaine[i], date=date_bilan[i])
            bilan.save()
            bilan_save = Bilan.objects.latest('id')
            workflow.bilan_semaine.add(bilan_save)
            workflow.save()

    context = {'reservation': reservations, 'form': form, 'workflow': workflow, 'annonce': annonce, 'address': myAdress}

    return render(request, 'compte/profile_annonce.html', context)