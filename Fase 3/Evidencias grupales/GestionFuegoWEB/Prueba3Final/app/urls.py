from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import BomberoView, VehiculoView, MecanicoView,InventarioView,SolicitudView,VehiculoEnEsperaView,BoletaView,VehiculoCompletoView,UsuarioView,SolicitudBomberoView

router = routers.DefaultRouter()
router.register(r'Vehiculo', VehiculoView)
router.register(r'Mecanico', MecanicoView)
router.register(r'Inventario', InventarioView)
router.register(r'Boleta', BoletaView)
router.register(r'vehiculos-en-espera',VehiculoEnEsperaView)
router.register(r'Bombero', BomberoView)
router.register(r'Vehiculo-Completo', VehiculoCompletoView)
router.register(r'Usuario', UsuarioView)
router.register(r'Solicitud-bombero', SolicitudBomberoView)

urlpatterns = [
    path('api/v1/', include(router.urls)),
   
]