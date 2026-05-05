from django.contrib import admin
from .models import Producto, Pedido, DetallePedido

# Registro básico
admin.site.register(Producto)

# Registro avanzado para ver los detalles dentro del pedido (Opcional pero recomendado)
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_creacion', 'completado', 'total']
    list_filter = ['completado', 'fecha_creacion']
    inlines = [DetallePedidoInline]
# Register your models here.