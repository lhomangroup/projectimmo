# Generated by Django 4.2.5 on 2024-11-06 00:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=10)),
                ('photo_profil', models.ImageField(blank=True, upload_to='')),
                ('photo_identite', models.ImageField(blank=True, upload_to='')),
                ('photo_stream', models.ImageField(blank=True, upload_to='')),
                ('packages_type', models.CharField(choices=[('BRON', 'Bronze'), ('SILV', 'Silver'), ('GOLD', 'Gold')], default='BRON', max_length=4, verbose_name='Package')),
                ('typelocataire', models.CharField(choices=[('PART', 'Particulier'), ('PROF', 'Profesionnel')], default='PART', max_length=4, verbose_name='Type de loueur')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('account', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rue', models.CharField(blank=True, max_length=20)),
                ('voie', models.CharField(blank=True, max_length=35)),
                ('ville', models.CharField(blank=True, max_length=20)),
                ('region', models.CharField(blank=True, max_length=20)),
                ('zipCode', models.CharField(blank=True, max_length=5)),
                ('pays', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
