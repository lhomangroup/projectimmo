
from django.core.management.base import BaseCommand
from account.models import Account
from client.models import Client

class Command(BaseCommand):
    help = 'Crée un utilisateur propriétaire'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email de l\'utilisateur')
        parser.add_argument('--password', type=str, default='password123', help='Mot de passe (défaut: password123)')
        parser.add_argument('--first_name', type=str, default='Propriétaire', help='Prénom')
        parser.add_argument('--last_name', type=str, default='Test', help='Nom')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']

        # Vérifier si l'utilisateur existe déjà
        if Account.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'⚠ L\'utilisateur {email} existe déjà')
            )
            return

        # Créer l'utilisateur
        user = Account.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            typelocataire='PROF',  # Professionnel pour propriétaire
            is_active=True
        )

        # Créer le profil Client associé
        Client.objects.create(
            user=user,
            nom=f'{first_name} {last_name}',
            type_utilisateur='proprietaire'
        )

        self.stdout.write(
            self.style.SUCCESS(f'✓ Utilisateur propriétaire créé avec succès!')
        )
        self.stdout.write(f'  - Email: {email}')
        self.stdout.write(f'  - Mot de passe: {password}')
        self.stdout.write(f'  - Type: Professionnel (Propriétaire)')
        self.stdout.write(f'  - Actif: Oui')
