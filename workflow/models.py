from django.db import models
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

# Create your models here.
from django.conf import settings


class AdressWorkflow(models.Model):

    rue = models.CharField(blank=True, max_length=20)
    voie = models.CharField(blank=True, max_length=35)
    ville = models.CharField(blank=True, max_length=20)
    region = models.CharField(blank=True, max_length=20)
    zipCode = models.CharField(blank=True, max_length=5)
    pays = models.CharField(blank=True, max_length=20)

class Commentaire_nek(models.Model):
    commentaire = models.TextField()

class Commentaire_demeya(models.Model):
    commentaire = models.TextField()

class Bilan(models.Model):
    date = models.DateTimeField(null=True)
    commentaire = models.TextField()

class File(models.Model):
    nom = models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)
    VISITE_SELECT = (
        ('0', 'Visites substituées'),
        ('1', 'Visites physiques'),
    )
    type_visite = models.CharField(max_length=30, null=True, choices=VISITE_SELECT)
    JOURS = ((1,'Lundi'),
             (2,'Mardi'),
             (3,'Mercredi'),
             (4, 'Jeudi'),
             (5, 'Vendredi'),
             (6, 'Samedi'),
             (7, 'Dimanche'))

    # planificateur_visite = MultiSelectField(_('Jour Preference'), choices=JOURS, blank=True, null=True)
    heure_debut = models.TimeField(null=True)
    heure_fin = models.TimeField(null=True)
    telephone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    date_reunion = models.DateTimeField(null=True)

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
    address = models.OneToOneField(
        AdressWorkflow,
        on_delete=models.CASCADE,
        null=True,
    )

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
    typeBien = models.CharField(max_length=100, blank=True, null=True)
    budgetLoyer = models.IntegerField(blank=False, null=True)
    SalaireFoyer = models.IntegerField(blank=False, null=True)
    motifDemenag = models.TextField(max_length=3000, blank=True, null=True)
    precisRecherche = models.TextField(max_length=3000, blank=True, null=True)
    document_avis = models.FileField(blank=True, null=True,
                                     upload_to='documents/',
                                     verbose_name="Pièce 1: Avis d'impot, attestation d'emplyeur ou contrat de travail")
    document_paye = models.FileField(blank=True, null=True,
                                     upload_to='documents/',
                                     verbose_name="Pièce 2: 3 dernières fiches de payes, pièces d'identité")
    document_quittance = models.FileField(blank=True, null=True,
                                          upload_to='documents/',
                                          verbose_name="Pièce 3: 3 dernières quittance de loyers")

    commentaire_nek = models.ManyToManyField(
        Commentaire_nek,
        null=True,
    )
    commentaire_demaya = models.ManyToManyField(
        Commentaire_demeya,
        null=True,
    )
    bilan_semaine = models.ManyToManyField(
        Bilan,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        unique=False
    )
    class Verdict_choice(models.TextChoices):
        accepte = 'acct', _('Accepté')
        attente = 'attn', _('Attente')
        refuse = 'refu', _('Refusé')


    verdict = models.CharField(
        max_length=4,
        choices=Verdict_choice.choices,
        default=Verdict_choice.refuse,
        verbose_name='Verdict'
    )


