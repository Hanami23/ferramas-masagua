from django.contrib import admin
from .models import Tipo, Producto, Boleta, DetalleBoleta

# Register your models here.
admin.site.register(Tipo)
admin.site.register(Producto)
admin.site.register(Boleta)
admin.site.register(DetalleBoleta)