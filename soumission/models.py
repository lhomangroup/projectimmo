from django.db import models
from django.utils.html import format_html
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField


class PlanningPla(models.Model):
    pla_id = models.AutoField(primary_key=True)
    pla_intitule = models.CharField(
        max_length=100, unique=True, blank=False, null=False, verbose_name='Jour')

    class Meta:
        managed = True
        db_table = 'planning_pla'
        verbose_name = 'Planning'

    def __str__(self):
        return self.pla_intitule

    def __unicode__(self):
        return


class checkboxcourse1(models.Model):
    cb1_id = models.AutoField(primary_key=True)
    coursename1 = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'CheckBox1_Cli'
        verbose_name = 'check box courses'


class BilanBil(models.Model):
    bil_id = models.AutoField(primary_key=True)
    cli = models.ForeignKey('ClientCli', models.DO_NOTHING,
                            blank=True, null=True, verbose_name='Client')
    bil_commentaire = models.TextField(
        blank=True, null=True, verbose_name='Bilan semaine')
    bil_date = models.DateTimeField(blank=True, null=True, verbose_name='Date')

    class Meta:
        managed = True
        db_table = 'bilan_bil'
        verbose_name = 'Bilan'


CLIENT_TYPE = [('pack dossier', 'pack dossier'),
               ('pack visites', 'pack visites')]

SITUATION = [('Marié (e)', 'Marié (e)'), ('Divorcé (e)', 'Divorcé (e)'),
             ('Célibataire', 'Célibataire'), ('Séparé (e)', 'Séparé (e)'), ('Veuf (ve)', 'Veuf (ve)')]

CHOICE_PACK = [('pack dossier', 'pack dossier'),
               ('pack visites', 'pack visites')]
CHOICE_PLANNING = [(1, 'Lundi'),
                   (2, 'Mardi'),
                   (3, 'Mercrédi'),
                   (4, 'Jeudi'),
                   (5, 'Vendredi'), (6, 'Samedi'), (7, 'Dimanche')]

CHOICE_VISITE = [('visites substituées', 'visites substituées'),
                 ('visites physiques', 'visites physiques')]


class ClientCli(models.Model):
    cli_id = models.AutoField(primary_key=True)
    cli_nom = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Nom', )
    cli_prenom = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Prénom')
    cli_situation = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Situation matrimoniale', choices=SITUATION)
    cli_contact = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Contact')
    cli_email = models.EmailField(
        max_length=100, blank=False, null=True, verbose_name='Email')
    cli_noumber_of_pesons = models.IntegerField(
        verbose_name='Nombre de personne dans le foyer', blank=True, null=True)
    cli_adresse_professionnelle = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Adresse professionnelle')
    cli_pays = CountryField(
        verbose_name='Pays', null=True, blank=False, )
    cli_ville = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Ville')
    
    LIEU_RECHERCHE_CHOICES = [
        ('paris', 'Paris'),
        ('lyon', 'Lyon'),
        ('marseille', 'Marseille'),
        ('toulouse', 'Toulouse'),
        ('nice', 'Nice'),
        ('nantes', 'Nantes'),
        ('montpellier', 'Montpellier'),
        ('strasbourg', 'Strasbourg'),
        ('bordeaux', 'Bordeaux'),
        ('lille', 'Lille'),
        ('rennes', 'Rennes'),
        ('reims', 'Reims'),
        ('le_havre', 'Le Havre'),
        ('saint_etienne', 'Saint-Étienne'),
        ('toulon', 'Toulon'),
        ('grenoble', 'Grenoble'),
        ('dijon', 'Dijon'),
        ('angers', 'Angers'),
        ('nimes', 'Nîmes'),
        ('villeurbanne', 'Villeurbanne'),
        ('clermont_ferrand', 'Clermont-Ferrand'),
        ('aix_en_provence', 'Aix-en-Provence'),
        ('brest', 'Brest'),
        ('limoges', 'Limoges'),
        ('tours', 'Tours'),
        ('amiens', 'Amiens'),
        ('perpignan', 'Perpignan'),
        ('metz', 'Metz'),
        ('besancon', 'Besançon'),
        ('orleans', 'Orléans'),
        ('rouen', 'Rouen'),
        ('mulhouse', 'Mulhouse'),
        ('caen', 'Caen'),
        ('nancy', 'Nancy'),
        ('argenteuil', 'Argenteuil'),
        ('montreuil', 'Montreuil'),
        ('roubaix', 'Roubaix'),
        ('tourcoing', 'Tourcoing'),
        ('avignon', 'Avignon'),
        ('dunkerque', 'Dunkerque'),
        ('banlieue_parisienne', 'Banlieue parisienne'),
        ('ile_de_france', 'Île-de-France (hors Paris)'),
        ('autres', 'Autres villes'),
    ]
    
    cli_lieu_recherche = models.CharField(
        max_length=100, blank=False, null=True, choices=LIEU_RECHERCHE_CHOICES, verbose_name='Lieu de recherche')
    
    TYPE_BIEN_CHOICES = [
        ('studio', 'Studio'),
        ('t1', 'T1 (1 pièce)'),
        ('t2', 'T2 (2 pièces)'),
        ('t3', 'T3 (3 pièces)'),
        ('t4', 'T4 (4 pièces)'),
        ('t5', 'T5 (5 pièces)'),
        ('t6_plus', 'T6 et plus'),
        ('maison_2_pieces', 'Maison 2 pièces'),
        ('maison_3_pieces', 'Maison 3 pièces'),
        ('maison_4_pieces', 'Maison 4 pièces'),
        ('maison_5_pieces', 'Maison 5 pièces'),
        ('maison_6_pieces_plus', 'Maison 6 pièces et plus'),
        ('loft', 'Loft'),
        ('duplex', 'Duplex'),
    ]

    cli_type_bien = models.CharField(
        max_length=100, blank=False, null=False, choices=TYPE_BIEN_CHOICES, 
        help_text='Maison ou Appart et taille', verbose_name='Type de bien')
    cli_pack = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Pack', choices=CHOICE_PACK)
    cli_budget = models.DecimalField(
        max_digits=8, decimal_places=0, blank=False, null=True, verbose_name='Budget alloué')
    cli_salaire_total = models.DecimalField(
        max_digits=8, decimal_places=0, blank=False, null=True, verbose_name='Salaire total du foyer')
    cli_montant_declare = models.DecimalField(
        max_digits=8, decimal_places=0, blank=False, null=True,
        verbose_name="Montant declaré sur le dernier avis d'import")
    cli_type = models.CharField(
        verbose_name='Type visite', max_length=100, blank=False, choices=CHOICE_VISITE, null=True)
    cli_planning = models.ManyToManyField(
        PlanningPla, verbose_name='Planning', blank=False)
    cli_horaire_debut = models.TimeField(
        verbose_name='Heure début: créneau horaire de visite', blank=False, null=True)
    cli_horaire_fin = models.TimeField(
        verbose_name='Heure fin: créneau horaire de visite', blank=False, null=True)
    cli_motif = models.TextField(
        blank=False, null=True, verbose_name='Motif de déménagement')
    cli_document_avis = models.FileField(blank=False, null=True,
                                         upload_to='documents/',
                                         verbose_name="Pièce 1: Avis d'impot, attestation d'emplyeur ou contrat de travail", )
    cli_document_paye = models.FileField(blank=False, null=True,
                                         upload_to='documents/',
                                         verbose_name="Pièce 2: 3 dernières fiches de payes, pièces d'identité", )
    cli_document_quittance = models.FileField(blank=False, null=True,
                                              upload_to='documents/',
                                              verbose_name="Pièce 3: 3 dernières quittance de loyers", )
    cli_referent = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Referent')
    cli_decision_ok = models.BooleanField(
        blank=True, null=True, verbose_name='Décision')
    cli_decision_reunion = models.BooleanField(
        blank=True, null=True, verbose_name='Reunion')

    # cli_checkbox = models.ManyToManyField(
    # checkboxcourse1, verbose_name='Signer et Accepter les conditions', blank=False)

    @property
    def validate(self):
        html = '<input type="checkbox" value="Signer"/>Cocher pour signer votre contrat<input type="test" name="coursename"/><input type="submit" value="Insert Record"/>'.format(
            self.pk)

        return format_html(html)

    @property
    def reunion(self):
        html = '<input type="checkbox" value="Accepter les conditions"/>Accepter les conditions<input type="test" name="coursename"/><input type="submit" value="Insert Record"/>'.format(
            self.pk)

        return format_html(html)

    def __str__(self):
        return '{}{}'.format(self.cli_nom, self.cli_prenom)

    class Meta:
        managed = True
        db_table = 'client_cli'
        verbose_name = 'Client'


class checkboxcourses(models.Model):
    cb_id = models.AutoField(primary_key=True)
    cli = models.ForeignKey(ClientCli, models.DO_NOTHING,
                            blank=True, null=True, verbose_name='Client')
    coursename = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'CheckBox_Cli'
        verbose_name = 'check box courses'


class SignerCli(models.Model):
    cli_id = models.AutoField(primary_key=True)
    cli_nom = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Nom', )
    cli_prenom = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Prénom')
    cli_email = models.EmailField(
        max_length=100, blank=False, null=True, verbose_name='Email')
    cli_document_avis = models.FileField(blank=False, null=True,
                                         upload_to='documents/',
                                         verbose_name="Pièce 1: Avis d'impot, attestation d'emplyeur ou contrat de travail")

    class Meta:
        managed = True
        db_table = 'Signer_Cli'
        verbose_name = 'SignerClient'


CHOICE_DECISION = [('Ok', 'Ok'), ('Demande de reunion', 'Demande de reunion')]


class CommentaireDem(models.Model):
    dem_id = models.AutoField(primary_key=True)
    cli = models.ForeignKey(ClientCli, models.DO_NOTHING,
                            blank=True, null=True, verbose_name='Client')
    dem_commentaires = models.TextField(
        blank=True, null=True, verbose_name='Commentaire')
    dem_date_commentaire = models.DateTimeField(
        blank=True, null=True, verbose_name='Date', auto_now_add=True)
    dem_decision = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Decision', choices=CHOICE_DECISION)

    class Meta:
        managed = True
        db_table = 'commentaire_dem'
        verbose_name = 'Commentaire'


class RecommandationNek(models.Model):
    nek_id = models.AutoField(primary_key=True)
    cli = models.ForeignKey(ClientCli, models.DO_NOTHING,
                            blank=True, null=True, verbose_name='Client')
    nek_recommandation = models.TextField(
        blank=True, null=True, verbose_name='Recommandation')
    nek_date_recommandation = models.DateField(
        blank=True, null=True, verbose_name='Date', auto_now_add=True)
    nek_decision = models.CharField(
        max_length=100, blank=False, null=True, verbose_name='Decision', choices=CHOICE_DECISION)

    class Meta:
        managed = True
        db_table = 'recommandation_nek'
        verbose_name = 'Recommandation'


class VisiteVit(models.Model):
    vit_id = models.AutoField(primary_key=True)
    cli = models.ForeignKey(
        ClientCli, models.DO_NOTHING, blank=True, null=True, verbose_name='Client')
    vit_commentaire = models.TextField(
        blank=True, null=True, verbose_name='Commentaire')
    vit_bilan = models.TextField(
        blank=True, null=True, verbose_name='Bilan de la visite')
    vit_date = models.DateTimeField(
        blank=True, null=True, verbose_name='Date prevu de la visite')

    class Meta:
        managed = True
        db_table = 'visite_vit'
        verbose_name = 'Visite'