
from django.core.management.base import BaseCommand
from account.models import Account
from client.models import Client

class Command(BaseCommand):
    help = 'Corrige les problèmes d\'un utilisateur (active le compte et crée le profil Client)'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email de l\'utilisateur à corriger')

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            # Récupérer l'utilisateur
            user = Account.objects.get(email=email)
            self.stdout.write(f'Utilisateur trouvé: {user.email}')
            
            # 1. Activer le compte
            if not user.is_active:
                user.is_active = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS('✓ Compte activé avec succès')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠ Le compte était déjà actif')
                )
            
            # 2. Créer le profil Client s'il n'existe pas
            try:
                client = Client.objects.get(user=user)
                self.stdout.write(
                    self.style.WARNING('⚠ Le profil Client existe déjà')
                )
                self.stdout.write(f'  - Nom: {client.nom}')
                self.stdout.write(f'  - Type utilisateur: {client.get_type_utilisateur_display()}')
            except Client.DoesNotExist:
                # Créer le profil Client
                client = Client.objects.create(
                    user=user,
                    nom=user.email,
                    type_utilisateur='locataire',  # Valeur par défaut
                )
                self.stdout.write(
                    self.style.SUCCESS('✓ Profil Client créé avec succès')
                )
                self.stdout.write(f'  - Nom: {client.nom}')
                self.stdout.write(f'  - Type utilisateur: {client.get_type_utilisateur_display()}')
            
            # 3. Vérification finale
            self.stdout.write('\n--- État final de l\'utilisateur ---')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'Nom: {user.first_name} {user.last_name}')
            self.stdout.write(f'Actif: {user.is_active}')
            
            try:
                client = Client.objects.get(user=user)
                self.stdout.write(f'Profil Client: ✓ Existe')
                self.stdout.write(f'Type utilisateur: {client.get_type_utilisateur_display()}')
            except Client.DoesNotExist:
                self.stdout.write(f'Profil Client: ✗ N\'existe pas')
            
            self.stdout.write(
                self.style.SUCCESS('\n🎉 Tous les problèmes ont été corrigés ! L\'utilisateur peut maintenant se connecter.')
            )
                
        except Account.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'✗ Aucun utilisateur trouvé avec l\'email: {email}')
            )
