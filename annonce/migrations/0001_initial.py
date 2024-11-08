# Generated by Django 4.2.5 on 2024-11-06 00:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdressAnnonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rue', models.CharField(blank=True, max_length=20)),
                ('voie', models.CharField(blank=True, max_length=35)),
                ('ville', models.CharField(blank=True, max_length=20)),
                ('region', models.CharField(blank=True, max_length=20)),
                ('zipCode', models.CharField(blank=True, max_length=5)),
                ('pays', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hebergement_choice', models.CharField(choices=[('APPT', 'Appartemment'), ('MAIS', 'Maison'), ('STUD', 'Studio'), ('OTHR', 'Autre')], default='APPT', max_length=4, verbose_name="Type d'hébergement")),
                ('type_location_choices', models.CharField(choices=[('ENTR', 'Logement entier'), ('PRIV', 'Chambre privée'), ('PART', 'Chambre partagée')], default='ENTR', max_length=4, verbose_name='Location partielle ou totale')),
                ('categorie_logement', models.CharField(blank=True, max_length=50)),
                ('titre_logement', models.CharField(blank=True, max_length=50)),
                ('description', models.TextField(blank=True)),
                ('nombre_personne', models.IntegerField(blank=True, default=1, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)])),
                ('pieces_couchage', models.IntegerField(blank=True, default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('dureeLocationMini', models.CharField(blank=True, max_length=50, null=True)),
                ('dureeLocationMaxi', models.CharField(blank=True, max_length=50, null=True)),
                ('loyer_tc', models.FloatField(blank=True, max_length=50, null=True)),
                ('charges_loyer', models.FloatField(blank=True, max_length=50, null=True)),
                ('reserved', models.BooleanField(default=False)),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='annonce.adressannonce')),
            ],
        ),
        migrations.CreateModel(
            name='CategorieService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(blank=True, max_length=50, null=True)),
                ('categorie', models.CharField(choices=[('life', 'Lifestyle'), ('bien', 'Bien être'), ('quot', 'Services quotidiens'), ('lois', 'Loisirs'), ('trsp', 'Transports'), ('inst', 'Installation')], default='life', max_length=4, verbose_name='Categorie Service')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('annonce', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='annonce.annonce')),
                ('heure_arrivee_apres', models.CharField(choices=[('1', '12h00'), ('2', '12h30'), ('3', '13h00'), ('4', '13h30'), ('5', '14h00'), ('6', '14h30'), ('7', '15h00'), ('8', '15h30'), ('9', '16h00'), ('10', '16h30'), ('11', '17h00'), ('12', '17h30'), ('13', '18h00'), ('14', '18h30'), ('15', '19h00'), ('16', '19h30'), ('17', '20h00'), ('18', '20h30'), ('19', '21h00'), ('19', '21h30'), ('19', '22h00')], default='flexible', max_length=10, verbose_name="Heure d'arrivée(après)")),
                ('heure_arrivee_avant', models.CharField(choices=[('1', '14h00'), ('2', '14h30'), ('3', '15h00'), ('4', '15h30'), ('5', '16h00'), ('6', '16h30'), ('7', '17h00'), ('8', '17h30'), ('9', '18h00'), ('10', '18h30'), ('11', '19h00'), ('12', '19h30'), ('13', '20h00'), ('14', '20h30'), ('15', '21h00'), ('16', '21h30'), ('17', '22h00')], default='flexible', max_length=10, verbose_name="Heure d'arrivée(avant)")),
                ('heure_depart', models.CharField(choices=[('1', '9h00'), ('2', '9h30'), ('3', '10h00'), ('4', '10h30'), ('5', '11h00'), ('6', '11h30'), ('7', '12h00'), ('8', '12h30'), ('9', '13h00'), ('10', '13h30'), ('11', '14h00'), ('12', '14h30'), ('13', '15h00'), ('14', '15h30'), ('15', '16h00'), ('16', '16h30'), ('17', '17h00'), ('18', '17h30'), ('19', '18h00')], default='flexible', max_length=10, verbose_name='Heure de départ(avant)')),
                ('accessible_handicape', models.BooleanField(choices=[(True, 'Oui'), (False, 'Non')], default=1)),
                ('fumeur_accepte', models.BooleanField(choices=[(True, 'Oui'), (False, 'Non')], default=1)),
                ('animaux_accepte', models.BooleanField(choices=[(True, 'Oui'), (False, 'Non')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('annonce', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='annonce.annonce')),
                ('gaz', models.BooleanField(choices=[(True, 'Oui'), (False, 'Non')], default=1)),
                ('fumee', models.BooleanField(default=False, verbose_name='Détecteur de fumée')),
                ('carbone', models.BooleanField(default=False, verbose_name='Détecteur de monoxyde de carbone')),
                ('extincteur', models.BooleanField(default=False, verbose_name='Extincteur')),
                ('consommationNrj', models.IntegerField(blank=True, default=1)),
                ('emissionGaz', models.IntegerField(blank=True, default=1)),
                ('docPerformance', models.FileField(blank=True, upload_to='')),
                ('risqueNaturel', models.FileField(blank=True, upload_to='')),
                ('risquePlomb', models.FileField(blank=True, upload_to='')),
                ('interieurElecGaz', models.FileField(blank=True, upload_to='')),
                ('amianteDoc', models.FileField(blank=True, upload_to='')),
                ('copopriete', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ImageLogement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(upload_to='images/')),
                ('annonce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annonce.annonce')),
            ],
        ),
        migrations.CreateModel(
            name='Calendrier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendrier_debut', models.DateField(blank=True, null=True)),
                ('calendrier_fin', models.DateField(blank=True, null=True)),
                ('disponibilite', models.CharField(choices=[('disp', 'Disponible'), ('indp', 'Indisponible')], default='disp', max_length=4, verbose_name='Disponibilité')),
                ('annonce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annonce.annonce')),
            ],
        ),
        migrations.AddField(
            model_name='annonce',
            name='categorie_service',
            field=models.ManyToManyField(blank=True, to='annonce.categorieservice'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='charges',
            field=models.ManyToManyField(blank=True, to='annonce.charges'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='equipements',
            field=models.ManyToManyField(blank=True, to='annonce.equipements'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='reservation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_reserved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='annonce',
            name='services',
            field=models.ManyToManyField(blank=True, to='annonce.services'),
        ),
        migrations.AddField(
            model_name='annonce',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
