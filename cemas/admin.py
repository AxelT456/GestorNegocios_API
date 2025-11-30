from django.contrib import admin
from .models import Categoria, Producto, MovimientoFinanciero, Venta, DetalleVenta

# Esto nos permitirá ver las tablas en http://localhost:8000/admin/
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(MovimientoFinanciero)

# Configuración especial para ver el detalle DENTRO de la venta
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    inlines = [DetalleVentaInline]
    list_display = ['id', 'usuario', 'total', 'metodo_pago', 'fecha']