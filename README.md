🖋️ Studio Tattoo — Sistema de Gestión de Citas
📌 Descripción del Proyecto

Studio Tattoo es una aplicación web desarrollada con Django + Firebase Firestore, diseñada para gestionar usuarios y citas dentro de un estudio de tatuajes.

El sistema permite a los clientes:

Registrarse en la plataforma

Iniciar sesión de forma segura

Gestionar su perfil

Crear citas

Editar citas

Eliminar citas

Visualizar su historial

El proyecto integra autenticación de Django con almacenamiento en la nube mediante Google Firebase Firestore, combinando seguridad local y persistencia NoSQL.

👨‍💻 Equipo de Desarrollo

Proyecto desarrollado por:

Nicolas Ruiz

Juan Sacanambuy

Maycol Posada

Samuel Prieto

🎯 Objetivo del Sistema

Desarrollar una plataforma web que permita digitalizar la gestión de citas de un estudio de tatuajes, optimizando:

Organización del negocio

Experiencia del cliente

Control de información

Acceso seguro a datos

🧱 Arquitectura del Sistema
Cliente (Browser)
        │
        ▼
Django Framework
(Authentication + Views)
        │
        ▼
Firebase Firestore (NoSQL Cloud DB)

Tecnologías utilizadas
Tecnología	Uso
Django	Backend MVC
Firebase Admin SDK	Conexión con Firestore
Firestore	Base de datos NoSQL
SQLite	Usuarios Django
HTML	Interfaz
Python	Lógica del sistema
📂 Estructura del Proyecto
Proyecto Studio Tattoo/
│
├── firebase/
│   ├── firebase_config.py
│   ├── serviceAccountKey.json
│
├── usuarios/
│   ├── templates/
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── registro.html
│   │   └── citas/
│   │       ├── form.html
│   │       ├── listar.html
│   │       └── editar.html
│   ├── views.py
│   ├── urls.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── settings.py

⚙️ Instalación del Proyecto
1️⃣ Clonar repositorio
git clone https://github.com/tu-repositorio/studio-tattoo.git
cd studio-tattoo

2️⃣ Crear entorno virtual
python -m venv venv


Activar:

Windows:

venv\Scripts\activate


Linux / Mac:

source venv/bin/activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

📦 Dependencias
Django>=4.2
firebase-admin>=6.5.0
requests>=2.31.0
python-dotenv>=1.0.0
gunicorn>=21.2.0
psycopg2-binary>=2.9.9

🔥 Configuración Firebase
Paso 1 — Crear proyecto Firebase

Ir a Firebase Console

Crear proyecto

Activar Firestore Database

Paso 2 — Descargar credenciales

Descargar:

serviceAccountKey.json


Ubicar en:

firebase/serviceAccountKey.json

Paso 3 — Inicialización automática

El sistema detecta automáticamente las credenciales mediante:

initialize_firebase()


ubicado en:

firebase/firebase_config.py

🧑‍💻 Funcionalidades Implementadas
✅ Autenticación

Registro de usuarios

Login seguro

Logout

Validaciones de contraseña

✅ Dashboard

Muestra:

Nombre

Email

Fecha de registro

Datos Firestore

✅ CRUD de Citas
Acción	Descripción
Crear	Agendar nueva cita
Leer	Listar citas
Editar	Modificar cita
Eliminar	Borrar cita
🔐 Seguridad

Autenticación Django integrada

Decorador personalizado:

@login_required_firebase


Validación de propietario de citas

Protección CSRF

🌐 Rutas del Sistema
URL	Función
/registro/	Crear usuario
/login/	Iniciar sesión
/logout/	Cerrar sesión
/dashboard/	Panel principal
/citas/	Listar citas
/citas/crear/	Crear cita
/citas/editar/<id>	Editar cita
/citas/eliminar/<id>	Eliminar cita
🗄️ Base de Datos
Django (SQLite)

Usuarios

Sesiones

Autenticación

Firestore

Colecciones:

usuarios
citas


Ejemplo documento cita:

{
  "titulo": "Tatuaje brazo",
  "descripcion": "Diseño tribal",
  "estado": "Pendiente",
  "usuario_id": "correo@email.com"
}

📅 Cronograma del Proyecto
Semana	Actividad
1	Análisis del problema
2	Diseño del sistema
3	Configuración Django
4	Integración Firebase
5	Sistema de autenticación
6	CRUD de citas
7	Diseño interfaces
8	Pruebas y correcciones
9	Documentación
10	Entrega final
🧪 Pruebas

Ejecutar servidor:

python manage.py runserver


Abrir:

http://127.0.0.1:8000/login/

🚀 Mejoras Futuras

Panel administrador para tatuadores

Calendario visual

Notificaciones por correo

API REST

Deploy en AWS o GCP

Pagos online

⚠️ Problemas Comunes
Firebase no conecta

Verificar:

serviceAccountKey.json

Migraciones
python manage.py migrate

📄 Licencia

Proyecto académico — SENA ADSO.

⭐ Contribución

Proyecto desarrollado con fines educativos para aprendizaje de:

Django

Firebase

Arquitectura Web

Integración Cloud


| Día           | Actividades Realizadas                                                  | Responsable(s)                                  |
| ------------- | ----------------------------------------------------------------------- | ----------------------------------------------- |
| **Lunes**     | Desarrollo completo del **Front-End** y avance inicial del **Back-End** | **Maycol** (Front-End) / **Nicolás** (Back-End) |
| **Martes**    | Finalización del desarrollo del **Back-End**                            | **Juan** (Back-End)                             |
| **Miércoles** | Elaboración completa de la **Documentación del proyecto**               | **Samuel** (Documentación)                      |
