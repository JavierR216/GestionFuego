from django.db import models
from django.utils import timezone


class Vehiculo(models.Model):
    ESTADO_CHOICES = [
        ('esperando', 'Esperando'),
        ('completado', 'Completado'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    TIPO_VEHICULO_CHOICES = [
        ('Carro Bomba', 'Carro Bomba'),
        ('Carro Escala', 'Carro Escala'),
        ('Carro Aljibe', 'Carro Aljibe'),
        ('Carro de Rescate', 'Carro de Rescate'),
        ('Carro Forestal', 'Carro Forestal'),
        ('Carro HazMat', 'Carro HazMat'),
        ('Unidad de Rescate', 'Unidad de Rescate'),
        ('Ambulancia de Bomberos', 'Ambulancia de Bomberos'),
        ('Carro QR', 'Carro QR'),
    ]

    patente = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    fecha_llegada = models.DateField()
    fecha_salida = models.DateField()
    tipo_vehiculo = models.CharField(max_length=50, choices=TIPO_VEHICULO_CHOICES, default='Carro Bomba')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='esperando', db_index=True)
    reparacion = models.CharField(max_length=100)
    repuesto = models.ForeignKey('Inventario', on_delete=models.SET_NULL, null=True)
    monto_total = models.IntegerField(default=0)
    mecanico = models.ForeignKey('Mecanico', on_delete=models.SET_NULL, null=True)
    monto_mecanico = models.IntegerField(default=0)

    def calcular_fecha_salida(self):
        if self.estado == 'completado':
            self.fecha_salida = timezone.now()
            self.save()

    def save(self, *args, **kwargs):
        if self.estado == 'completado' and not self.fecha_salida:
            self.calcular_fecha_salida()
        super().save(*args, **kwargs)

class Mecanico(models.Model): ##MECANICOS
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    monto_mecanico = models.IntegerField(default=0)

class Inventario(models.Model): ##REPUESTOS
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    precio = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        super().save(*args, **kwargs)

class VehiculoEnEspera(models.Model):  
    tipo_vehiculo= models.CharField(max_length=50)
    patente = models.CharField(max_length=200)
    fecha_llegada = models.DateField()
    Reparación = models.CharField(max_length=100)
    repuesto = models.ForeignKey('Inventario', on_delete=models.SET_NULL, null=True)
    monto_total = models.IntegerField(default=0)
    mecanico = models.ForeignKey('Mecanico', on_delete=models.SET_NULL, null=True)
    monto_mecanico = models.IntegerField(default=0)
    

    def __str__(self):
        return self.patente


class Solicitud(models.Model):
    tipo_vehiculo = models.CharField(max_length=50)
    patente = models.CharField(max_length=200)
    fecha_llegada = models.DateField()
    reparacion = models.CharField(max_length=100)
    repuesto = models.ForeignKey('Inventario', on_delete=models.SET_NULL, null=True)
    precio_repuestos = models.IntegerField(default=0)
    mecanico = models.ForeignKey('Mecanico', on_delete=models.SET_NULL, null=True)
    monto_mecanico = models.IntegerField(default=0)
    monto_total = models.IntegerField(default=0)

    def calcular_precio_total(self):
        self.monto_total = self.precio_repuestos + self.monto_mecanico
        self.save()

    def formatear_moneda(self, valor):
        return f"${valor:,.0f}".replace(",", ".")

    def monto_total_formateado(self):
        return self.formatear_moneda(self.monto_total)

    def precio_repuestos_formateado(self):
        return self.formatear_moneda(self.precio_repuestos)

    def save(self, *args, **kwargs):
        self.calcular_precio_total()
        super().save(*args, **kwargs)
    
class Boleta(models.Model):
    tipo_vehiculo = models.CharField(max_length=50)
    patente = models.CharField(max_length=200)
    fecha_llegada = models.DateField()
    reparacion = models.CharField(max_length=100)
    repuesto = models.ForeignKey('Inventario', on_delete=models.SET_NULL, null=True)
    precio_repuestos = models.IntegerField(default=0)
    mecanico = models.ForeignKey('Mecanico', on_delete=models.SET_NULL, null=True)
    monto_mecanico = models.IntegerField(default=0)
    monto_total = models.IntegerField(default=0)

    

    def __str__(self):
        return self.patente
    
class Bombero(models.Model):
    nombre = models.CharField(max_length=100, default='Sin nombre')  # Se añade un valor por defecto
    descripcion = models.CharField(max_length=255, default='Sin descripción')

    def __str__(self):
        return self.nombre

class VehiculoCompleto(models.Model):
    tipo_vehiculo = models.CharField(max_length=50)
    patente = models.CharField(max_length=200)
    fecha_llegada = models.DateField()
    reparacion = models.CharField(max_length=100)
    mecanico = models.ForeignKey('Mecanico', on_delete=models.SET_NULL, null=True)
    monto_mecanico = models.IntegerField(default=0)
    monto_total = models.IntegerField(default=0)
    fecha_salida = models.DateField(null=True)

    def __str__(self):
        return self.patente
    
class Usuario(models.Model):
    usuario = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario
    
class SolicitudBombero(models.Model):
    bombero = models.CharField(max_length=50)
    tipo_vehiculo = models.CharField(max_length=50)
    patente = models.CharField(max_length=200)
    fecha_salida = models.DateField()

    def __str__(self):
        return self.bombero


