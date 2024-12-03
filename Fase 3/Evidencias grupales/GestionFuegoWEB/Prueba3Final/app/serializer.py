from rest_framework import serializers
from .models import Vehiculo, Mecanico, Inventario, Solicitud, VehiculoEnEspera,Boleta,Bombero,VehiculoCompleto,Usuario,SolicitudBombero
from datetime import datetime



class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class MecanicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mecanico
        fields = '__all__'

class BomberoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bombero
        fields = '__all__'

class VehiculoCompletoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiculoCompleto
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class SolicitudSerializer(serializers.ModelSerializer):
    repuesto_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Solicitud
        fields = '__all__'

    def create(self, validated_data):
        repuesto_id = validated_data.pop('repuesto_id', None)
        solicitud = Solicitud.objects.create(**validated_data)
        
        if repuesto_id:
            try:
                repuesto = Inventario.objects.get(id=repuesto_id)
                solicitud.repuesto = repuesto
                solicitud.precio_repuestos = repuesto.precio * validated_data.get('cantidad', 1)
                solicitud.save()

                repuesto.stock -= validated_data.get('cantidad', 1)
                repuesto.save()
            except Inventario.DoesNotExist:
                raise serializers.ValidationError("Repuesto no encontrado.")
        
        return solicitud

class VehiculoEnEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehiculoEnEspera
        fields = '__all__'
        
    def update(self, instance, validated_data):
        # Lógica personalizada si es necesario
        instance.repuesto = validated_data.get('repuesto', instance.repuesto)
        instance.save()
        return instance       

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = '__all__'  # Incluye todos los campos del modelo

    def validate_fecha_llegada(self, value):
        # Puedes agregar validaciones personalizadas si es necesario
        if value is None:
            raise serializers.ValidationError("La fecha de llegada no puede estar vacía")
        return value
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class SolicitudBomberoioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudBombero
        fields = '__all__'
