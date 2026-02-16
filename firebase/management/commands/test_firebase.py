from django.core.management.base import BaseCommand
from firebase.firebase_config import get_db


class Command(BaseCommand):
    help = 'Prueba la conexión con Firebase'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Prueba de Conexión Firebase + Django'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

        try:
            db = get_db()
            if db is not None:
                self.stdout.write(self.style.SUCCESS('✅ Conexión exitosa con Firebase'))
                self.stdout.write(self.style.SUCCESS('✅ Cliente de Firestore obtenido correctamente'))
                self.stdout.write(self.style.SUCCESS('\n' + '='*60))
                self.stdout.write(self.style.SUCCESS('Firebase está listo para usar en Django'))
                self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
            else:
                self.stdout.write(self.style.ERROR('✖️ Error: No se pudo obtener Firestore'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✖️ Error de conexión: {e}'))
