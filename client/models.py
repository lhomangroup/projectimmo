
from django.db import models
import datetime
# debut code pour User= Client
from django.conf import settings
# fin code pour User= Client
from django.utils.translation import gettext_lazy as _
from address.models import AddressField, Country, State


# Create your models here.
class Client(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE)
    nom=models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)
    telephone=models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_creation=models.DateTimeField(auto_now_add=True, null=True)
    class PackageChoices(models.TextChoices):
        PACK_DOSSIER = 'PDOS', _('Pack Dossier')
        PACK_VISITES = 'PVST', _('Pack Visite')
        PACK_BASIQUE = 'PBAS', _('Pack Basique')
        PACK_BOOSTER = 'PBST', _('Pack Booster')
        PACK_PREMIUM = 'PPRE', _('Pack Premium')
        PACK_CONCIERGERIE = 'PCNC', _('Pack Conciergerie')

    package_choice = models.CharField(
        max_length=4,
        choices=PackageChoices.choices,
        default=PackageChoices.PACK_DOSSIER,
        verbose_name='Confirmer votre pack'
    )
    personne_foyer = models.IntegerField(blank=True, null=True, verbose_name='Nombre de personnes dans le foyer')
    address1 = AddressField(blank=True, null=True, verbose_name='Adresse')
    address2 = AddressField(related_name='+', blank=True, null=True, verbose_name='')
    city = AddressField(related_name='states', blank=True, null=True, verbose_name='Ville')
    postalCode = AddressField(related_name='localities_country', blank=True, null=True, verbose_name='Code Postal')
    country = AddressField(related_name='country', blank=True, null=True, verbose_name='Pays')
    class SituationMatrimo_choices(models.TextChoices):
        MARRIE = 'MARR', _('Marrié (e)')
        DIVORCE = 'DIVO', _('Divorcé (e)')
        CELIBATAIRE = 'CELI', _('Célibataire')
        SEPARE = 'SEPA', _('Séparé (e)')
        VEUF = 'VEUF', _('Veuf (ve)')

    situation_matrimo = models.CharField(
        max_length=4,
        choices=SituationMatrimo_choices.choices,
        default=SituationMatrimo_choices.CELIBATAIRE,
        verbose_name='Situation matrimoniale'
    )
    referent = models.CharField(max_length=100, blank=True, null=True)
    lieuRecherche = models.CharField(max_length=100, blank=True, null=True)
    typeBien= models.CharField(max_length=100, blank=True, null=True)
    budgetLoyer = models.IntegerField(blank=False, null=True)
    SalaireFoyer = models.IntegerField(blank=False, null=True)
    motifDemenag = models.TextField(max_length=3000, blank=True, null=True)
    precisRecherche = models.TextField(max_length=3000, blank=True, null=True)
    document_avis = models.FileField(blank=True, null=True,
                                         upload_to='documents/', verbose_name="Pièce 1: Avis d'impot, attestation d'emplyeur ou contrat de travail")
    document_paye = models.FileField(blank=True, null=True,
                                         upload_to='documents/', verbose_name="Pièce 2: 3 dernières fiches de payes, pièces d'identité")
    document_quittance = models.FileField(blank=True, null=True,
                                              upload_to='documents/', verbose_name="Pièce 3: 3 dernières quittance de loyers")

def __str__(self):
    return self.nom

class Meta:
    managed = True
    db_table = 'client'
    verbose_name = 'Client'
