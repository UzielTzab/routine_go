from django.core.management.base import BaseCommand
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Crea o asegura que exista el usuario de pruebas'

    def handle(self, *args, **options):
        email = 'test@uzielos.com'
        password = 'password123'
        
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Usuario {email} creado exitosamente.'))
        else:
            # Aseguramos que tenga el password correcto
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.WARNING(f'Usuario {email} ya existía. Contraseña actualizada.'))
