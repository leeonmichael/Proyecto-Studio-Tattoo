from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.inicar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('citas/', views.agendar_cita, name='agendar_cita'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('citas/editar/<str:cita_id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<str:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
]