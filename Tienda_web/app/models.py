import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Marca(models.Model):
    nomb_marca = models.CharField( max_length=50)

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField()
    imagen1 = models.ImageField( upload_to='add_producto', null=True) 
    imagen2 = models.ImageField( upload_to='add_producto', null=True)
    imagen3 = models.ImageField( upload_to='add_producto', null=True)
    imagen4 = models.ImageField( upload_to='add_producto', null=True)
    imagen5 = models.ImageField( upload_to='add_producto', null=True)
    marca = models.ForeignKey(Marca ,on_delete=models.CASCADE)
    def __str__(self) :
        return self.nombre
    
class Boleta (models.Model):
    ESTADOS_BOLETA = [
            ('pendiente', 'Pendiente'),
            ('enviado', 'Enviado'),
            ('entregado', 'Entregado'),
            ('cancelado', 'Cancelado')
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fechaVenta = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(User,on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADOS_BOLETA, default='pendiente')
    def __str__(self):
            return str(self.id)
    @property
    def get_total(self):
        detalle = self.detalle_boleta_set.all()
        total = sum([item.producto.precio * item.cantidad_productos for item in detalle])
        return total
    @property
    def get_item(self):
        detalle = self.detalle_boleta_set.all()
        total = sum([item.cantidad_productos for item in detalle])
        return total
    
class Detalle_boleta (models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    cantidad_productos = models.IntegerField(default=0) 
    def __str__(self):
        return str(self.boleta.id) + '-' + self.producto.nombre
    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad_productos
        return total
