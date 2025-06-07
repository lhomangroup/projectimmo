from django.utils.translation import gettext_lazy as _

from django.db import models
from django.conf import settings
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import CheckboxSelectMultiple

# Create your models here.
class AdressAnnonce(models.Model):

    rue = models.CharField(blank=True, max_length=20)
    voie = models.CharField(blank=True, max_length=35)
    ville = models.CharField(blank=True, max_length=20)
    region = models.CharField(blank=True, max_length=20)
    zipCode = models.CharField(blank=True, max_length=5)
    pays = models.CharField(blank=True, max_length=20)

class Equipements(models.Model):
    nom = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nom

class CategorieService(models.Model):
    nom = models.CharField(max_length=200, null=True)

class Services(models.Model):
    nom = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=50, blank=True, null=True)

    class Categorie(models.TextChoices):
        Lifestyle = 'life', _('Lifestyle')
        Bien_etre = 'bien', _('Bien être')
        Services_quotidien = 'quot', _('Services quotidiens')
        Loisirs = 'lois', _('Loisirs')
        Transport = 'trsp', _('Transports')
        Installation = 'inst', _('Installation')

    categorie = models.CharField(
        max_length=4,
        choices=Categorie.choices,
        default=Categorie.Lifestyle,
        verbose_name="Categorie Service"
    )
    def __str__(self):
        return self.nom


class Charges(models.Model):
    nom = models.CharField(max_length=200, null=True, unique=True)

    def __str__(self):
        return self.nom

class Annonce(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        unique=False
    )
    class TypeHebergement(models.TextChoices):
        Appartemment = 'APPT', _('Appartemment')
        Maison = 'MAIS', _('Maison')
        Studio = 'STUD', _('Studio')
        Autre = 'OTHR', _('Autre')

    hebergement_choice = models.CharField(
        max_length=4,
        choices=TypeHebergement.choices,
        default=TypeHebergement.Appartemment,
        verbose_name="Type d'hébergement"
    )

    class TypeLocation(models.TextChoices):
        logement_entier = 'ENTR', _('Logement entier')
        chambre_privee = 'PRIV', _('Chambre privée')
        chambre_partagee = 'PART', _('Chambre partagée')

    type_location_choices = models.CharField(
        max_length=4,
        choices=TypeLocation.choices,
        default=TypeLocation.logement_entier,
        verbose_name="Location partielle ou totale"
    )

    categorie_logement = models.CharField(max_length=50, blank=True)
    titre_logement = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    nombre_personne = IntegerField(
        default=1,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ],
        blank=True
    )
    pieces_couchage = IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        blank=True
    )
    equipements = models.ManyToManyField(Equipements, blank=True)
    services = models.ManyToManyField(Services, blank=True)
    categorie_service = models.ManyToManyField(CategorieService, blank=True)
    charges = models.ManyToManyField(Charges, blank=True)
    dureeLocationMini = models.CharField(blank=True,null=True, max_length=50)
    dureeLocationMaxi = models.CharField(blank=True,null=True, max_length=50)
    loyer_tc = models.FloatField(max_length=50, blank=True, null=True)
    charges_loyer = models.FloatField(max_length=50, blank=True, null=True)
    reservation = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        unique=False,
        related_name = 'user_reserved'
    )
    reserved = models.BooleanField(default=False)
    address = models.OneToOneField(
        AdressAnnonce,
        on_delete=models.CASCADE,
        null=True,
    )

class ImageLogement(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    images = models.FileField(upload_to='images/')

class Calendrier(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    calendrier_debut = models.DateField(blank=True, null=True)
    calendrier_fin = models.DateField(blank=True, null=True)
    class Disponibilité(models.TextChoices):
        disponible = 'disp', _('Disponible')
        indisponible = 'indp', _('Indisponible')

    disponibilite = models.CharField(
        max_length=4,
        choices=Disponibilité.choices,
        default=Disponibilité.disponible,
        verbose_name="Disponibilité"
    )

class Condition(models.Model):
    annonce = models.OneToOneField(
        Annonce,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    CHOICES_APRES = (
        ('1', '12h00'),
        ('2', '12h30'),
        ('3', '13h00'),
        ('4', '13h30'),
        ('5', '14h00'),
        ('6', '14h30'),
        ('7', '15h00'),
        ('8', '15h30'),
        ('9', '16h00'),
        ('10', '16h30'),
        ('11', '17h00'),
        ('12', '17h30'),
        ('13', '18h00'),
        ('14', '18h30'),
        ('15', '19h00'),
        ('16', '19h30'),
        ('17', '20h00'),
        ('18', '20h30'),
        ('19', '21h00'),
        ('19', '21h30'),
        ('19', '22h00'),
    )

    heure_arrivee_apres = models.CharField(
        max_length=10,
        choices=CHOICES_APRES,
        default="flexible",
        verbose_name="Heure d'arrivée(après)"
    )
    CHOICES_AVANT = (
        ('1', '14h00'),
        ('2', '14h30'),
        ('3', '15h00'),
        ('4', '15h30'),
        ('5', '16h00'),
        ('6', '16h30'),
        ('7', '17h00'),
        ('8', '17h30'),
        ('9', '18h00'),
        ('10', '18h30'),
        ('11', '19h00'),
        ('12', '19h30'),
        ('13', '20h00'),
        ('14', '20h30'),
        ('15', '21h00'),
        ('16', '21h30'),
        ('17', '22h00'),
    )
    heure_arrivee_avant = models.CharField(
        max_length=10,
        choices=CHOICES_AVANT,
        default="flexible",
        verbose_name="Heure d'arrivée(avant)"
    )

    CHOICES_DEPART = (
        ('1','9h00'),
        ('2','9h30'),
        ('3','10h00'),
        ('4','10h30'),
        ('5','11h00'),
        ('6','11h30'),
        ('7','12h00'),
        ('8','12h30'),
        ('9', '13h00'),
        ('10', '13h30'),
        ('11', '14h00'),
        ('12', '14h30'),
        ('13', '15h00'),
        ('14', '15h30'),
        ('15', '16h00'),
        ('16', '16h30'),
        ('17', '17h00'),
        ('18', '17h30'),
        ('19', '18h00'),
    )

    heure_depart = models.CharField(
        max_length=10,
        choices=CHOICES_DEPART,
        default="flexible",
        verbose_name="Heure de départ(avant)"
    )

    choice_bool = [(True, 'Oui'), (False, 'Non')]
    accessible_handicape = models.BooleanField(choices=choice_bool, default=1)
    fumeur_accepte = models.BooleanField(choices=choice_bool, default=1)
    animaux_accepte = models.BooleanField(choices=choice_bool, default=1)

class Equipement(models.Model):
    annonce = models.OneToOneField(
        Annonce,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # Vous pouvez ajouter d'autres champs d'équipement ici selon vos besoins
    # Par exemple :
    # wifi = models.BooleanField(default=False)
    # television = models.BooleanField(default=False)
    # lave_vaisselle = models.BooleanField(default=False)
    # etc.

class Diagnostic(models.Model):
    annonce = models.OneToOneField(
        Annonce,
        on_delete=models.CASCADE,
        primary_key=True,
        default='',
    )
    choice_bool = [(True, 'Oui'), (False, 'Non')]
    gaz = models.BooleanField(choices=choice_bool, default=1)
    fumee = models.BooleanField('Détecteur de fumée', default=False)
    carbone = models.BooleanField('Détecteur de monoxyde de carbone', default=False)
    extincteur = models.BooleanField('Extincteur', default=False)
    consommationNrj = models.IntegerField(default=1, blank=True)
    emissionGaz = models.IntegerField(default=1, blank=True)
    docPerformance = models.FileField(blank=True)
    risqueNaturel = models.FileField(blank=True)
    risquePlomb = models.FileField(blank=True)
    interieurElecGaz = models.FileField(blank=True)
    amianteDoc = models.FileField(blank=True)
    copopriete = models.FileField(blank=True)