from django.apps import AppConfig


class FirebaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firebase'
    
    def ready(self):
        """Se ejecuta cuando Django está listo"""
        print("\n" + "="*60)
        print("App Firebase inicializada correctamente")
        print("="*60 + "\n")
