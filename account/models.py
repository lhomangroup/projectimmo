
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, telephone, first_name, last_name, typelocataire, password=None):
        if not email:
            raise ValueError("Entrez une adresse mail")
        if not telephone:
            raise ValueError("Entrez un nom de téléphone")
        if not last_name:
            raise ValueError("Entrez un nom de famille")
        if not first_name:
            raise ValueError("Entrez un prénom")
        if not typelocataire:
            raise ValueError("Entrez un type de locataire")

        user = self.model(
            email = self.normalize_email(email),
            telephone = telephone,
            first_name = first_name,
            last_name = last_name,
            typelocataire = typelocataire,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, telephone, typelocataire, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            first_name = first_name,
            last_name = last_name,
            telephone = telephone,
            typelocataire = typelocataire,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=10)
    photo_profil = models.ImageField(blank=True)
    photo_identite = models.ImageField(blank=True)
    photo_stream = models.ImageField(blank=True)

    class TypePackages(models.TextChoices):
        bronze = 'BRON', _('Bronze')
        silver = 'SILV', _('Silver')
        gold = 'GOLD', _('Gold')

    packages_type = models.CharField(
        max_length=4,
        choices=TypePackages.choices,
        default=TypePackages.bronze,
        verbose_name="Package"
    )
    class TypeLocataire(models.TextChoices):
        particulier = 'PART', _('Particulier')
        profesionnel = 'PROF', _('Profesionnel')

    typelocataire = models.CharField(
        max_length=4,
        choices=TypeLocataire.choices,
        default=TypeLocataire.particulier,
        verbose_name="Type de loueur"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','telephone','typelocataire']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Address(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
        default='',
    )
    rue = models.CharField(blank=True, max_length=20)
    voie = models.CharField(blank=True, max_length=35)
    ville = models.CharField(blank=True, max_length=20)
    region = models.CharField(blank=True, max_length=20)
    zipCode = models.CharField(blank=True, max_length=5)
    pays = models.CharField(blank=True, max_length=20)

