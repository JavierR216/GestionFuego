from django.contrib import admin
from .models import Vehiculo,Mecanico,Inventario,Solicitud,VehiculoEnEspera,Boleta,Bombero,VehiculoCompleto,Usuario,SolicitudBombero
# Register your models here.
admin.site.register(Vehiculo)
admin.site.register(Mecanico)
admin.site.register(Inventario)
admin.site.register(VehiculoEnEspera)
admin.site.register(Boleta)
admin.site.register(Bombero)
admin.site.register(VehiculoCompleto)
admin.site.register(Usuario)
admin.site.register(SolicitudBombero)