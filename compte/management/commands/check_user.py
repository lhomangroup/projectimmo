
from django.core.management.base import BaseCommand
from account.models import Account
from client.models import Client

class Command(BaseCommand):
    help = 'Vérifie si un utilisateur existe dans la base de données'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email de l\'utilisateur à vérifier')

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            # Vérifier dans le modèle Account
            user = Account.objects.get(email=email)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Utilisateur trouvé dans Account:')
            )
            self.stdout.write(f'  - ID: {user.id}')
            self.stdout.write(f'  - Email: {user.email}')
            self.stdout.write(f'  - Nom: {user.first_name} {user.last_name}')
            self.stdout.write(f'  - Téléphone: {user.telephone}')
            self.stdout.write(f'  - Type de locataire: {user.get_typelocataire_display()}')
            self.stdout.write(f'  - Package: {user.get_packages_type_display()}')
            self.stdout.write(f'  - Actif: {user.is_active}')
            self.stdout.write(f'  - Staff: {user.is_staff}')
            self.stdout.write(f'  - Admin: {user.is_admin}')
            self.stdout.write(f'  - Date de création: {user.date_joined}')
            self.stdout.write(f'  - Dernière connexion: {user.last_login}')
            
            # Vérifier s'il a un profil Client associé
            try:
                client = Client.objects.get(user=user)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Profil Client associé trouvé:')
                )
                self.stdout.write(f'  - Nom client: {client.nom}')
                self.stdout.write(f'  - Type utilisateur: {client.get_type_utilisateur_display()}')
                self.stdout.write(f'  - Date de création: {client.date_creation}')
            except Client.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING('⚠ Aucun profil Client associé trouvé')
                )
                
        except Account.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'✗ Aucun utilisateur trouvé avec l\'email: {email}')
            )
            
            # Proposer de lister tous les utilisateurs
            self.stdout.write('\nUtilisateurs existants dans la base:')
            users = Account.objects.all()
            if users:
                for user in users:
                    self.stdout.write(f'  - {user.email} ({user.first_name} {user.last_name})')
            else:
                self.stdout.write('  Aucun utilisateur dans la base de données')
