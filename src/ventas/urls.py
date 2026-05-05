from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('procesar/', views.procesar_pedido, name='procesar_pedido'),
]