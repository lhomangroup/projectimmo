from pyexpat.errors import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.baseconv import base64
from django.views import View
from django.utils import timezone

from .models import Annonce, ImageLogement, AdressAnnonce, Condition, Equipement, PlanPaiementCaution, PaiementMensuelCaution
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
from .forms import AnnonceForm, LoggedForm, CreateUserForm, DescriptionForm, FormLoyer, FormEquipement, CategorieServicesForm, FormCalendrier, FormCondition, VerifImage, ServicesForm, FormDiagnostic, UserModif, PlanPaiementCautionForm, PaiementMensuelForm
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
    from django.contrib import messages

    form = AnnonceForm()
    userForm = CreateUserForm()

    if request.method == 'POST':
        userForm = CreateUserForm(request.POST)
        annonceForm = AnnonceForm(request.POST)

        rue = request.POST.get('rue', '')
        voie = request.POST.get('voie', '')
        ville = request.POST.get('ville', '')
        region = request.POST.get('region', '')
        zip = request.POST.get('zip', '')
        pays = request.POST.get('pays', 'France')

        print(f"Formulaire utilisateur valide: {userForm.is_valid()}")
        print(f"Formulaire annonce valide: {annonceForm.is_valid()}")

        if not userForm.is_valid():
            print("Erreurs formulaire utilisateur:", userForm.errors)
            messages.error(request, f"Erreur dans les informations utilisateur: {userForm.errors}")

        if not annonceForm.is_valid():
            print("Erreurs formulaire annonce:", annonceForm.errors)
            messages.error(request, f"Erreur dans les informations de l'annonce: {annonceForm.errors}")

        # - validate both forms
        if userForm.is_valid() and annonceForm.is_valid():
            try:
                # Créer l'utilisateur
                user = userForm.save()
                user.is_active = True
                user.save()
                print(f"Utilisateur créé: {user.email}")

                # Créer l'adresse
                myAdress = AdressAnnonce.objects.create(
                    rue=rue,
                    voie=voie,
                    ville=ville,
                    region=region,
                    zipCode=zip,
                    pays=pays
                )
                print(f"Adresse créée: ID {myAdress.id}")

                # Créer l'annonce
                annonce = annonceForm.save(commit=False)
                annonce.user = user
                annonce.address = myAdress
                annonce.save()
                print(f"Annonce créée: ID {annonce.id}")

                # Gérer l'upload d'images multiples
                uploaded_images = request.FILES.getlist('images')
                for image in uploaded_images:
                    ImageLogement.objects.create(
                        annonce=annonce,
                        images=image
                    )
                print(f"{len(uploaded_images)} images uploadées")

                # Créer les objets associés
                Condition.objects.create(annonce=annonce)
                Address.objects.create(account=user)
                print("Objets associés créés")

                # Envoi d'email de confirmation
                try:
                    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={
                        'uidb64': uidb64, 
                        'token': token_generator.make_token(user)
                    })
                    activate_url = 'http://' + domain + link

                    email_subject = 'Activez votre compte'
                    email_body = f'Bonjour {user.first_name},\n\nCliquez sur ce lien pour activer votre compte:\n{activate_url}'

                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@lhoman.com',
                        [user.email],
                    )
                    email.send(fail_silently=False)
                    print("Email envoyé avec succès")

                    messages.success(request, f'Annonce créée avec succès ! Un email de confirmation a été envoyé à {user.email}')
                    return redirect('creer-annonce')

                except Exception as e:
                    print(f"Erreur envoi email: {e}")
                    messages.warning(request, f'Annonce créée avec succès ! Cependant, l\'email de confirmation n\'a pas pu être envoyé.')
                    return redirect('creer-annonce')

            except Exception as e:
                print(f"Erreur lors de la création: {e}")
                messages.error(request, f'Erreur lors de la création de l\'annonce: {e}')

    else:
        userForm = CreateUserForm()
        annonceForm = AnnonceForm()

    context = {'annonceForm': annonceForm, 'userForm': userForm}
    return render(request, 'annonce/creer-annonce.html', context)

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

                # CORRECTION: Activer automatiquement le compte
                user.is_active = True
                user.save()

                return redirect('acces')
    context={'form':form}
    return render(request,'compte/inscription.html',context)

@unauthenticated_user
def login_user(request):
    from django.views.decorators.csrf import csrf_protect
    from django.contrib import messages

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print(f"Tentative de connexion pour: {email}")

        # Vérifier que l'utilisateur existe
        try:
            from account.models import Account
            user_exists = Account.objects.filter(email=email).first()
            if user_exists:
                print(f"Utilisateur trouvé: {user_exists.email}, actif: {user_exists.is_active}")
            else:
                print(f"Aucun utilisateur trouvé avec l'email: {email}")
                messages.error(request, 'Aucun compte trouvé avec cet email.')
                context = {}
                return render(request, 'compte/login-annonce.html', context)
        except Exception as e:
            print(f"Erreur lors de la vérification utilisateur: {e}")

        user = authenticate(request, email=email, password=password)
        print(f"Résultat authentication: {user}")

        if user is not None:
            if user.is_active:
                login(request, user)
                print(f"Connexion réussie pour: {user.email}")
                
                # Rediriger selon le type d'utilisateur
                if user.typelocataire == 'PART':  # Particulier (locataire)
                    return redirect('dashboard-list')
                else:  # Professionnel (propriétaire/agent)
                    return redirect('dashboard-list')
            else:
                print(f"Utilisateur inactif: {user.email}")
                messages.error(request, 'Votre compte n\'est pas activé.')
        else:
            print(f"Échec de l'authentification pour: {email}")
            messages.error(request, 'Email ou mot de passe incorrect.')

    context = {}
    return render(request, 'compte/login-annonce.html', context)

def logout_annonce(request):
    logout(request)
    return redirect('annonceHome')

@login_required(login_url='login-annonce')
def logged_annonce(request):
    # Vérifier que l'utilisateur est un professionnel
    if request.user.typelocataire == 'PART':  # Si c'est un particulier (locataire)
        return redirect('dashboard-list')  # Le rediriger vers le dashboard
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

            # Gérer l'upload d'images multiples
            print("Traitement des images uploadées...")
            uploaded_images = request.FILES.getlist('images')
            for image in uploaded_images:
                ImageLogement.objects.create(
                    annonce=annonce,
                    images=image
                )
            print(f"{len(uploaded_images)} images uploadées avec succès")

            # Créer une condition pour cette annonce
            print("Création de la condition...")
            Condition.objects.create(annonce=annonce)
            print("Condition créée avec succès")

            # Créer un équipement pour cette annonce
            print("Création de l'équipement...")
            Equipement.objects.create(annonce=annonce)
            print("Équipement créé avec succès")

            return redirect('dashboard-list')
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
    annonces = Annonce.objects.filter(user=request.user).order_by('-id')
    context = {'annonces': annonces}
    return render(request, 'annonce/dashboard/dashboard_list.html', context)

@login_required
def dashboard_list(request):
    """Vue principale du tableau de bord listant les annonces selon le type d'utilisateur"""
    print(f"Dashboard_list appelé pour l'utilisateur: {request.user.email}")
    print(f"Utilisateur authentifié: {request.user.is_authenticated}")
    print(f"Type d'utilisateur: {request.user.get_typelocataire_display()}")
    print(f"Type d'utilisateur code: {request.user.typelocataire}")

    if request.user.typelocataire == 'PART':  # Particulier (locataire)
        print("Utilisateur identifié comme PARTICULIER (locataire)")
        # Vérifier s'il y a une annonce sélectionnée pour ce locataire
        annonce_selectionnee = Annonce.objects.filter(locataire_interesse=request.user).first()

        if annonce_selectionnee:
            print(f"Annonce sélectionnée trouvée: {annonce_selectionnee.titre_logement}")
            # Afficher l'annonce sélectionnée avec option d'annulation
            template = 'annonce/dashboard/dashboard_locataire.html'
            context = {
                'annonce_selectionnee': annonce_selectionnee,
                'is_locataire': True
            }
        else:
            print("Aucune annonce sélectionnée, affichage de toutes les annonces")
            # Afficher toutes les annonces disponibles pour les locataires
            annonces = Annonce.objects.filter(locataire_interesse__isnull=True).order_by('-id')
            template = 'annonce/search/annonce_result.html'
            context = {'annonces': annonces, 'is_locataire': True}
    elif request.user.typelocataire == 'PROF':  # Professionnel (propriétaire/agent)
        print("Utilisateur identifié comme PROFESSIONNEL (propriétaire)")
        # Afficher seulement leurs propres annonces
        annonces = Annonce.objects.filter(user=request.user).order_by('-id')
        template = 'annonce/dashboard/dashboard_list.html'
        context = {'annonces': annonces, 'is_locataire': False}

        for annonce in annonces:
            print(f"Annonce ID: {annonce.id}, Titre: {annonce.titre_logement}")
    else:
        print(f"Type d'utilisateur non reconnu: {request.user.typelocataire}")
        # Par défaut, traiter comme propriétaire
        annonces = Annonce.objects.filter(user=request.user).order_by('-id')
        template = 'annonce/dashboard/dashboard_list.html'
        context = {'annonces': annonces, 'is_locataire': False}

    print(f"Template utilisé: {template}")
    print(f"Nombre d'annonces trouvées: {len(context.get('annonces', [context.get('annonce_selectionnee')] if context.get('annonce_selectionnee') else []))}")
    return render(request, template, context)

@login_required
def description_view(request, pk):
    myObject = Annonce.objects.get(id=pk)
    requete = request.user
    myAdress = myObject.address

    if request.method == 'POST':
        form = DescriptionForm(request.POST, instance=myObject)

        # Récupérer les données d'adresse
        rue = request.POST.get('rue', '')
        voie = request.POST.get('voie', '')
        ville = request.POST.get('ville', '')
        region = request.POST.get('region', '')
        zip = request.POST.get('zip', '')
        pays = request.POST.get('pays', 'France')
        address = request.POST.get('adressComplete')

        if form.is_valid():
            # Sauvegarder l'annonce
            form.save()

            # Mettre à jour l'adresse si les champs d'adresse sont fournis
            if address:
                if myAdress:
                    myAdress.rue = rue
                    myAdress.voie = voie
                    myAdress.ville = ville
                    myAdress.region = region
                    myAdress.zipCode = zip
                    myAdress.pays = pays
                    myAdress.save()
                else:
                    # Créer une nouvelle adresse si elle n'existe pas
                    from annonce.models import AdressAnnonce
                    myAdress = AdressAnnonce.objects.create(
                        rue=rue,
                        voie=voie,
                        ville=ville,
                        region=region,
                        zipCode=zip,
                        pays=pays
                    )
                    myObject.address = myAdress
                    myObject.save()

            return redirect(request.META.get('HTTP_REFERER', '/annonce/dashboard/list/'))
        else:
            print("Erreurs du formulaire:", form.errors)
    else:
        form = DescriptionForm(instance=myObject)

    context = {'form': form, 'obj': myObject, 'requete': requete, 'address': myAdress}
    return render(request,'annonce/dashboard/description.html',context)

@login_required
def equipment_view(request, pk):
    annonce = Annonce.objects.get(id=pk)

    # Créer l'objet Equipement s'il n'existe pas
    myEquipement, created = Equipement.objects.get_or_create(annonce=annonce)

    form = FormEquipement(instance=myEquipement)

    if request.method == 'POST':
        form = FormEquipement(request.POST, instance=myEquipement)
        if form.is_valid():
            form.save()
            return redirect('dashboard-annonce', pk=annonce.id)

    context = {'form': form, 'annonce': annonce}
    return render(request, 'annonce/dashboard/equipment.html', context)

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

    try:
        myAdress = Address.objects.get(account=user)
    except Address.DoesNotExist:
        # Créer une adresse vide si elle n'existe pas
        myAdress = Address.objects.create(account=user)

    if request.method == 'POST':
        form = UserModif(request.POST, instance=user)
        rue = request.POST.get('rue', '')
        voie = request.POST.get('voie', '')
        ville = request.POST.get('ville', '')
        region = request.POST.get('region', '')
        zip_code = request.POST.get('zip', '')
        pays = request.POST.get('pays', '')
        address_complete = request.POST.get('adressComplete', '')

        if form.is_valid():
            # Sauvegarder les informations utilisateur
            form.save()

            # Mettre à jour l'adresse si des données sont fournies
            if any([rue, voie, ville, region, zip_code, pays]):
                myAdress.rue = rue
                myAdress.voie = voie
                myAdress.ville = ville
                myAdress.region = region
                myAdress.zipCode = zip_code
                myAdress.pays = pays
                myAdress.save()

            return redirect('dashboard-annonce', pk=myObject.id)
    else:
        form = UserModif(instance=user)

    context = {'form': form, 'obj': myObject, 'address': myAdress}
    return render(request, 'annonce/dashboard/userDashboard.html', context)

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

def user_coord_dashboard(request, pk):
    myObject = get_object_or_404(Annonce, pk=pk)
    myAdress = myObject.address

    if request.method == 'POST':
        form = UserModif(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/annonce/dashboard/list/'))
    else:
        form = UserModif(instance=request.user)

    context = {'form': form, 'obj': myObject, 'address': myAdress}
    return render(request, 'annonce/dashboard/usercoord.html', context)

def detail_annonce(request, pk):
    """Vue pour afficher les détails d'une annonce publique"""
    annonce = get_object_or_404(Annonce, pk=pk)
    images = ImageLogement.objects.filter(annonce=annonce)

    context = {
        'annonce': annonce,
        'images': images,
        'address': annonce.address
    }
    return render(request, 'annonce/detail_annonce.html', context)

@login_required
def selectionner_annonce(request, pk):
    """Vue pour qu'un locataire sélectionne une annonce pour soumission de dossier"""
    if request.user.typelocataire != 'PART':
        return redirect('dashboard-list')

    annonce = get_object_or_404(Annonce, pk=pk)

    # Vérifier que l'annonce n'est pas déjà sélectionnée par un autre locataire
    if annonce.locataire_interesse and annonce.locataire_interesse != request.user:
        from django.contrib import messages
        messages.error(request, 'Cette annonce est déjà sélectionnée par un autre locataire.')
        return redirect('dashboard-list')

    # Désélectionner toute autre annonce de ce locataire
    Annonce.objects.filter(locataire_interesse=request.user).update(locataire_interesse=None)

    # Sélectionner cette annonce
    annonce.locataire_interesse = request.user
    annonce.save()

    from django.contrib import messages
    messages.success(request, f'Annonce "{annonce.titre_logement}" sélectionnée. Vous pouvez maintenant soumettre votre dossier.')
    return redirect('dashboard-list')

@login_required
def annuler_selection_annonce(request, pk):
    """Vue pour qu'un locataire annule la sélection d'une annonce"""
    if request.user.typelocataire != 'PART':
        return redirect('dashboard-list')

    annonce = get_object_or_404(Annonce, pk=pk, locataire_interesse=request.user)
    annonce.locataire_interesse = None
    annonce.save()

    from django.contrib import messages
    messages.success(request, 'Sélection annulée. Vous pouvez maintenant choisir une autre annonce.')
    return redirect('dashboard-list')

@login_required
def supprimer_annonce(request, pk):
    """Vue pour supprimer une annonce (pour les propriétaires)"""
    from django.contrib import messages
    import os
    
    annonce = get_object_or_404(Annonce, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire de l'annonce
    if annonce.user != request.user:
        messages.error(request, 'Vous n\'êtes pas autorisé à supprimer cette annonce.')
        return redirect('dashboard-list')
    
    if request.method == 'POST':
        titre_annonce = annonce.titre_logement
        
        try:
            # Supprimer les images associées
            images = ImageLogement.objects.filter(annonce=annonce)
            for image in images:
                # Supprimer le fichier physique
                if image.images:
                    try:
                        if os.path.isfile(image.images.path):
                            os.remove(image.images.path)
                    except Exception as e:
                        print(f"Erreur suppression fichier image: {e}")
                image.delete()
            
            # Supprimer les objets liés manuellement si nécessaire
            try:
                if hasattr(annonce, 'condition'):
                    annonce.condition.delete()
            except:
                pass
                
            try:
                if hasattr(annonce, 'equipement'):
                    annonce.equipement.delete()
            except:
                pass
                
            try:
                if hasattr(annonce, 'address'):
                    annonce.address.delete()
            except:
                pass
            
            # Supprimer l'annonce
            annonce.delete()
            
            messages.success(request, f'L\'annonce "{titre_annonce}" a été supprimée avec succès.')
            print(f"Annonce {pk} supprimée avec succès")
            
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            messages.error(request, f'Erreur lors de la suppression: {e}')
        
        return redirect('dashboard-list')
    
    context = {'annonce': annonce}
    return render(request, 'annonce/dashboard/supprimer_annonce.html', context)

@login_required
def ajouter_au_tableau_de_bord(request, pk):
    """Vue pour qu'un locataire ajoute une annonce à son tableau de bord"""
    if request.user.typelocataire != 'PART':
        from django.contrib import messages
        messages.error(request, 'Seuls les locataires peuvent ajouter des annonces à leur tableau de bord.')
        return redirect('detail-annonce', pk=pk)

    annonce = get_object_or_404(Annonce, pk=pk)

    # Vérifier que l'annonce n'est pas déjà sélectionnée par un autre locataire
    if annonce.locataire_interesse and annonce.locataire_interesse != request.user:
        from django.contrib import messages
        messages.error(request, 'Cette annonce est déjà sélectionnée par un autre locataire.')
        return redirect('detail-annonce', pk=pk)

    # Désélectionner toute autre annonce de ce locataire
    Annonce.objects.filter(locataire_interesse=request.user).update(locataire_interesse=None)

    # Sélectionner cette annonce
    annonce.locataire_interesse = request.user
    annonce.save()

    from django.contrib import messages
    messages.success(request, f'L\'annonce "{annonce.titre_logement}" a été ajoutée à votre tableau de bord.')
    return redirect('dashboard-list')

@unauthenticated_user
def inscription_simple(request):
    """Vue pour l'inscription simple sans création d'annonce"""
    from django.contrib import messages

    if request.method == 'POST':
        userForm = CreateUserForm(request.POST)
        if userForm.is_valid():
            user = userForm.save(commit=False)
            # Gérer le type d'utilisateur
            type_utilisateur = userForm.cleaned_data.get('type_utilisateur')
            if type_utilisateur == 'proprietaire':
                user.typelocataire = 'PROP'
            elif type_utilisateur == 'partenaire':
                user.typelocataire = 'PART'
            # Pour les locataires, garder la valeur du champ typelocataire
            user.save()
            username = userForm.cleaned_data.get('email')
            messages.success(request, f'Compte créé pour {username}!')
            return redirect('login-annonce')
    else:
        userForm = CreateUserForm()

    context = {'userForm': userForm}
    return render(request, 'annonce/inscription-simple.html', context)


@login_required
def creer_plan_paiement_caution(request, pk):
    """Créer un plan de paiement pour la caution d'une annonce"""
    annonce = get_object_or_404(Annonce, pk=pk)
    
    # Vérifier que l'utilisateur est le locataire intéressé
    if request.user.typelocataire != 'PART' or annonce.locataire_interesse != request.user:
        from django.contrib import messages
        messages.error(request, 'Vous n\'êtes pas autorisé à créer un plan de paiement pour cette annonce.')
        return redirect('dashboard-list')
    
    # Vérifier qu'il n'y a pas déjà un plan de paiement
    if hasattr(annonce, 'plan_paiement_caution'):
        from django.contrib import messages
        messages.info(request, 'Un plan de paiement existe déjà pour cette annonce.')
        return redirect('voir_plan_paiement_caution', pk=annonce.plan_paiement_caution.id)
    
    if request.method == 'POST':
        form = PlanPaiementCautionForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.annonce = annonce
            plan.locataire = request.user
            plan.save()
            
            # Créer les mensualités automatiquement
            from datetime import date, timedelta
            from dateutil.relativedelta import relativedelta
            
            date_debut = date.today() + relativedelta(months=1)  # Premier paiement le mois suivant
            
            for i in range(plan.nombre_mensualites):
                PaiementMensuelCaution.objects.create(
                    plan_paiement=plan,
                    numero_mensualite=i + 1,
                    montant=plan.montant_mensuel,
                    date_echeance=date_debut + relativedelta(months=i)
                )
            
            from django.contrib import messages
            messages.success(request, f'Plan de paiement créé avec succès! {plan.nombre_mensualites} mensualités de {plan.montant_mensuel:.2f}€')
            return redirect('voir_plan_paiement_caution', pk=plan.id)
    else:
        form = PlanPaiementCautionForm()
    
    context = {
        'form': form,
        'annonce': annonce
    }
    return render(request, 'annonce/paiement/creer_plan_caution.html', context)

@login_required
def voir_plan_paiement_caution(request, pk):
    """Voir les détails d'un plan de paiement caution"""
    plan = get_object_or_404(PlanPaiementCaution, pk=pk)
    
    # Vérifier les permissions
    if request.user != plan.locataire and request.user != plan.annonce.user:
        from django.contrib import messages
        messages.error(request, 'Vous n\'êtes pas autorisé à voir ce plan de paiement.')
        return redirect('dashboard-list')
    
    paiements = plan.paiements_mensuels.all()
    
    # Calculer les statistiques
    paiements_payes = paiements.filter(statut='PAYE').count()
    montant_total_paye = sum(p.montant for p in paiements if p.statut == 'PAYE')
    montant_restant = plan.montant_caution_total - montant_total_paye
    
    context = {
        'plan': plan,
        'paiements': paiements,
        'paiements_payes': paiements_payes,
        'montant_total_paye': montant_total_paye,
        'montant_restant': montant_restant,
        'pourcentage_completion': (paiements_payes / plan.nombre_mensualites * 100) if plan.nombre_mensualites > 0 else 0
    }
    return render(request, 'annonce/paiement/voir_plan_caution.html', context)

@login_required
def effectuer_paiement_mensuel(request, pk):
    """Marquer un paiement mensuel comme effectué"""
    paiement = get_object_or_404(PaiementMensuelCaution, pk=pk)
    
    # Vérifier que l'utilisateur est le locataire
    if request.user != paiement.plan_paiement.locataire:
        from django.contrib import messages
        messages.error(request, 'Vous n\'êtes pas autorisé à effectuer ce paiement.')
        return redirect('dashboard-list')
    
    if request.method == 'POST':
        form = PaiementMensuelForm(request.POST, instance=paiement)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.statut = 'PAYE'
            paiement.date_paiement = timezone.now()
            paiement.save()
            
            from django.contrib import messages
            messages.success(request, f'Paiement de la mensualité {paiement.numero_mensualite} confirmé!')
            return redirect('voir_plan_paiement_caution', pk=paiement.plan_paiement.id)
    else:
        form = PaiementMensuelForm(instance=paiement)
    
    context = {
        'form': form,
        'paiement': paiement
    }
    return render(request, 'annonce/paiement/effectuer_paiement.html', context)

@login_required
def liste_plans_paiement_proprietaire(request):
    """Liste des plans de paiement pour un propriétaire"""
    if request.user.typelocataire == 'PART':
        return redirect('dashboard-list')
    
    annonces = Annonce.objects.filter(user=request.user)
    plans = PlanPaiementCaution.objects.filter(annonce__in=annonces).order_by('-date_creation')
    
    context = {'plans': plans}
    return render(request, 'annonce/paiement/liste_plans_proprietaire.html', context)
