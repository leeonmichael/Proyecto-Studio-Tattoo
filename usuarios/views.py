from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from functools import wraps
from firebase_admin import firestore
from firebase.firebase_config import initialize_firebase
import requests
import os 

# Inicializar Firebase
try:
    initialize_firebase()
    db = firestore.client()
    firebase_enabled = True
except Exception as e:
    db = None
    firebase_enabled = False
    print(f"Advertencia: Firebase no está completamente inicializado: {e}")

def registro_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # Validaciones
        if not nombre or not email or not password:
            mensaje = "Por favor completa todos los campos obligatorios"
            return render(request, 'registro.html', {'mensaje': mensaje})
        
        if password != password_confirm:
            mensaje = "Las contraseñas no coinciden"
            return render(request, 'registro.html', {'mensaje': mensaje})
        
        if len(password) < 8:
            mensaje = "La contraseña debe tener mínimo 8 caracteres"
            return render(request, 'registro.html', {'mensaje': mensaje})
        
        try:
            # Verificar si el usuario ya existe en Django
            if User.objects.filter(username=email).exists():
                mensaje = "El email ya está registrado"
                return render(request, 'registro.html', {'mensaje': mensaje})
            
            # Crear usuario en Django
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombre
            )
            
            # Intentar guardar en Firestore si Firebase está disponible
            if firebase_enabled and db:
                try:
                    db.collection('usuarios').document(user.username).set({
                        'nombre': nombre,
                        'email': email,
                        'telefono': telefono,
                        'rol': 'cliente',
                        'usuario_django_id': user.id,
                        'fecha_registro': firestore.SERVER_TIMESTAMP
                    })
                    print(f"✅ Usuario {email} guardado en Firestore")
                except Exception as firestore_error:
                    print(f"⚠️ Advertencia al guardar en Firestore: {firestore_error}")
                    # No detenemos el flujo si falla Firestore
            
            mensaje = "✅ Usuario registrado exitosamente. ¡Bienvenido!"
            
        except Exception as e:
            mensaje = f"Error al registrar usuario: {str(e)}"
            print(f"Error en registro: {e}")

        return render(request, 'registro.html', {'mensaje': mensaje})
    
    return render(request, 'registro.html')

#Logica para iniciar sesion
def login_required_firebase(view_func):
    """
    Este decorador verifica si el usuario está autenticado con Django.
    Si no lo está, redirige al usuario a la página de inicio de sesión.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Acceso denegado. Por favor inicia sesión.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

 
# Vista para el inicio de sesión - USANDO DJANGO AUTH
def inicar_sesion(request):
    # Si ya está autenticado, redirige al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        # Validaciones
        if not email or not password:
            messages.error(request, "Por favor completa todos los campos")
            return render(request, 'login.html')
        
        try:
            # Buscar usuario por email (ya que username es email en nuestro sistema)
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Iniciar sesión
                login(request, user)
                messages.success(request, f"✅ ¡Bienvenido {user.first_name}!")
                return redirect('dashboard')
            else:
                messages.error(request, "❌ Email o contraseña incorrectos")
        except Exception as e:
            messages.error(request, f"Error al iniciar sesión: {str(e)}")
    
    return render(request, 'login.html')

def cerrar_sesion(request):
    """Cierra la sesión del usuario"""
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

@login_required_firebase # Verifica que el usuario esta loggeado 
def dashboard(request):
    """
    Panel principal. Solo es accesible si el usuario está autenticado.
    Recuperamos los datos del usuario autenticado.
    """
    user = request.user
    datos_usuario = {
        'nombre': user.first_name or user.username,
        'email': user.email,
        'usuario_id': user.id,
        'fecha_registro': user.date_joined,
    }
    
    # Intentar obtener datos adicionales de Firestore si están disponibles
    if firebase_enabled and db:
        try:
            doc_ref = db.collection('usuarios').document(user.username)
            doc = doc_ref.get()
            if doc.exists:
                firestore_data = doc.to_dict()
                datos_usuario.update(firestore_data)
                print(f"✅ Datos obtenidos de Firestore para {user.email}")
        except Exception as e:
            print(f"⚠️ No se pudieron obtener datos de Firestore: {e}")
            # Continuamos con los datos de Django si falla Firestore
    
    return render(request, 'dashboard.html', {'datos_usuario': datos_usuario})    

@login_required_firebase
def agendar_cita(request):
    """
    READ: Recuperar las citas del usuario desde firestore
    """

    uid = request.user.username

    citas = []

    try:
        # Vamos a filtrar las citas del usuario
        docs = db.collection('citas').where('usuario_id', '==', uid).stream()
        for doc in docs:
            cita = doc.to_dict()
            cita['id'] = doc.id
            citas.append(cita)
    except Exception as e:
        messages.error(request, f"Hubo un error al obtener las citas: {e}")
    
    return render(request, 'citas/listar.html', {'citas' : citas})

@login_required_firebase # Verifica que el usuario esta loggeado
def crear_cita(request):
    """
    CREATE: Reciben los datos desde el formulario y se almacenan
    """
    if (request.method == 'POST'):
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        uid = request.user.username  # Usa el email del usuario autenticado

        try:
            db.collection('citas').add({
                'titulo': titulo,
                'descripcion': descripcion,
                'estado': 'Pendiente',
                'usuario_id': uid,
                'fecha_creacion': firestore.SERVER_TIMESTAMP
            })
            messages.success(request, "✅ Cita creada con éxito")
            return redirect('agendar_cita')
        except Exception as e:
            messages.error(request, f"Error al crear la cita: {e}")
        
    return render(request, 'citas/form.html')

@login_required_firebase # Verifica que el usuario esta loggeado
def eliminar_cita(request, cita_id):
    """
    DELETE: Eliminar un documento especifico por id
    """
    try:
        db.collection('citas').document(cita_id).delete()
        messages.success(request, "🗑️ Cita eliminada.")
    except Exception as e:
        messages.error(request, f"Error al eliminar: {e}")

    return redirect('agendar_cita')
    
@login_required_firebase # Verifica que el usuario esta loggeado
def editar_cita(request, cita_id):
    """
    UPDATE: Recupera los datos de la cita especifica y actualiza los campos en firebase
    """
    uid = request.user.username
   
    cita_ref = db.collection('citas').document(cita_id)

    try:
        doc = cita_ref.get()
        if not doc.exists:
            messages.error(request, "La cita no existe")
            return redirect('agendar_cita')
        
        cita_data = doc.to_dict()

        if cita_data.get('usuario_id') != uid:
            messages.error(request, "❌ No tienes permiso para editar esta cita")
            return redirect('agendar_cita')
        
        if request.method == 'POST':
            nuevo_titulo = request.POST.get('titulo')
            nueva_desc = request.POST.get('descripcion')
            nuevo_estado = request.POST.get('estado')

            cita_ref.update({
                'titulo': nuevo_titulo,
                'descripcion': nueva_desc,
                'estado': nuevo_estado,
                'fecha_actualizacion': firestore.SERVER_TIMESTAMP
            })

            messages.success(request, "✅ Cita actualizada correctamente.")
            return redirect('agendar_cita')
    except Exception as e:
        messages.error(request, f"Error al editar la cita: {e}")
        return redirect('agendar_cita')
    
    return render(request, 'citas/editar.html', {'cita': cita_data, 'id': cita_id})