from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vehiculo, Mecanico, Inventario, Solicitud, VehiculoEnEspera,Boleta,Bombero,VehiculoCompleto,Usuario,SolicitudBombero
from .serializer import VehiculoSerializer, MecanicoSerializer, InventarioSerializer, SolicitudSerializer, VehiculoEnEsperaSerializer,BoletaSerializer,BomberoSerializer,VehiculoCompletoSerializer,UsuarioSerializer,SolicitudBomberoioSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction

class VehiculoView(viewsets.ModelViewSet):
    serializer_class = VehiculoSerializer
    queryset = Vehiculo.objects.all()

class MecanicoView(viewsets.ModelViewSet):
    serializer_class = MecanicoSerializer
    queryset = Mecanico.objects.all()

class BomberoView(viewsets.ModelViewSet):
    serializer_class = BomberoSerializer
    queryset = Bombero.objects.all()    

class VehiculoCompletoView(viewsets.ModelViewSet):
    serializer_class = VehiculoCompletoSerializer
    queryset = VehiculoCompleto.objects.all()

class InventarioView(viewsets.ModelViewSet):
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all()

class BoletaView(viewsets.ModelViewSet):
    serializer_class = BoletaSerializer
    queryset = Boleta.objects.all()

class SolicitudView(viewsets.ModelViewSet):
    serializer_class = SolicitudSerializer
    queryset = Solicitud.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        repuesto_id = request.data.get('repuesto')
        cantidad = int(request.data.get('cantidad', 1))
        tipo_vehiculo = request.data.get('tipo_vehiculo')
        patente = request.data.get('patente')
        reparacion = request.data.get('reparacion')
        mecanico_id = request.data.get('mecanico')

        repuesto = get_object_or_404(Inventario, id=repuesto_id)
        if repuesto.stock < cantidad:
            return Response({'error': 'Stock insuficiente para el repuesto solicitado.'}, status=status.HTTP_400_BAD_REQUEST)

        mecanico = get_object_or_404(Mecanico, id=mecanico_id)
        precio_repuestos = repuesto.precio * cantidad

        try:
            with transaction.atomic():
                solicitud = Solicitud.objects.create(
                    tipo_vehiculo=tipo_vehiculo,
                    patente=patente,
                    reparacion=reparacion,
                    repuesto=repuesto,
                    cantidad=cantidad,
                    precio_repuestos=precio_repuestos,
                    mecanico=mecanico
                )
                repuesto.stock -= cantidad
                repuesto.save()

                serializer = SolicitudSerializer(solicitud)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Error al crear la solicitud: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VehiculoEnEsperaView(viewsets.ModelViewSet):
    serializer_class = VehiculoEnEsperaSerializer
    queryset = VehiculoEnEspera.objects.all()

    @action(detail=True, methods=['put'])
    def asignar_repuesto(self, request, pk=None):
        # Obtén el vehículo en espera por pk
        try:
            vehiculo = VehiculoEnEspera.objects.get(pk=pk)
        except VehiculoEnEspera.DoesNotExist:
            return Response({"detail": "Vehículo en espera no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Obtener el repuesto del request
        repuesto_id = request.data.get('repuesto')
        if repuesto_id:
            try:
                repuesto = Inventario.objects.get(pk=repuesto_id)
                vehiculo.Repuesto = repuesto
                vehiculo.save()
                return Response({"detail": "Repuesto asignado correctamente"}, status=status.HTTP_200_OK)
            except Inventario.DoesNotExist:
                return Response({"detail": "Repuesto no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Faltan datos para asignar el repuesto"}, status=status.HTTP_400_BAD_REQUEST)

class UsuarioView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

class SolicitudBomberoView(viewsets.ModelViewSet):
    serializer_class = SolicitudBomberoioSerializer
    queryset = SolicitudBombero.objects.all()