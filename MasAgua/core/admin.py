from django.contrib import admin
from .models import TipoAgua, Producto, Boleta, DetalleBoleta

# Register your models here.
admin.site.register(TipoAgua)
admin.site.register(Producto)
admin.site.register(Boleta)
admin.site.register(DetalleBoleta)