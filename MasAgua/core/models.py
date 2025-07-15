from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tipo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre del tipo')

    def __str__(self):
        return self.nombre
    
 #aqui se agregan los productos ej: agua de botella 2000clp   
class Producto(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre del Producto')
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  # << imagen
    stock = models.PositiveIntegerField(default=0)  # <-- campo de stock agregado

    def __str__(self):
        return f"{self.descripcion} - ${self.precio}"

#aqui generamos las boletas 
    
class Boleta(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En camino'),
        ('entregado', 'Entregado'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_entrega = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')  # ✅ nuevo campo

    def __str__(self):
        return f"Boleta #{self.id} - {self.usuario.username} - {self.estado_entrega}"

class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, related_name='detalles', on_delete=models.CASCADE)
    descripcionCompra = models.CharField(max_length=200)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)