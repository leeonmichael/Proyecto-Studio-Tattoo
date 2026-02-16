from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.inicar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]