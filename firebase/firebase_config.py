import os
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Variable global
_db = None


def initialize_firebase():
    """Inicializa Firebase y retorna el cliente de Firestore"""
    global _db
    
    try:
        # Verificar si ya está inicializado
        if firebase_admin._apps:
            _db = firestore.client()
            print("✅ Firebase ya estaba inicializado")
            return _db
        
        # Obtener la ruta base (directorio del proyecto)
        base_dir = Path(__file__).resolve().parent.parent
        
        # Buscar la ruta del certificado en varias ubicaciones posibles
        possible_paths = [
            base_dir / 'firebase' / 'serviceAccountKey.json',  # firebase/serviceAccountKey.json
            base_dir / 'serviceAccountKey.json',                 # serviceAccountKey.json en raíz
        ]
        
        cert_path = None
        for path in possible_paths:
            if path.exists():
                cert_path = path
                break
        
        if not cert_path:
            print(f"\n📍 Rutas buscadas:")
            for path in possible_paths:
                print(f"   - {path}")
            raise FileNotFoundError(f"❌ No se encontró serviceAccountKey.json en ninguna ubicación esperada")
        
        print(f"📁 Credenciales encontradas en: {cert_path}")
        
        # Inicializar Firebase
        cred = credentials.Certificate(str(cert_path))
        firebase_admin.initialize_app(cred)
        
        # Obtener cliente de Firestore
        _db = firestore.client()
        print("✅ Firebase SDK inicializado correctamente")
        print("✅ Conexión con Firestore establecida")
        
        return _db
        
    except Exception as e:
        print(f"❌ Error al inicializar Firebase: {e}")
        return None


def get_db():
    """Retorna la instancia de Firestore"""
    global _db
    if _db is None:
        initialize_firebase()
    return _db


if __name__ == "__main__":
    initialize_firebase() 