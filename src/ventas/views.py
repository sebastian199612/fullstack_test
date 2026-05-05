from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Producto, Pedido, DetallePedido

# 1. Vista para mostrar la lista de productos
def lista_productos(request):
    productos = Producto.objects.all()
    # Usamos render porque necesitamos mostrar un HTML complejo
    return render(request, 'ventas.html', {'productos': productos})

# 2. Vista para agregar productos al carrito
def agregar_al_carrito(request, producto_id):
    # Intentamos obtener el producto, si no existe lanza error 404
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Manejo de lógica de sesión para el carrito
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        carrito[producto_id_str] += 1
    else:
        carrito[producto_id_str] = 1

    request.session['carrito'] = carrito
    
    
    return HttpResponse(f"Producto {producto.nombre} añadido. <a href='/ventas/productos'>Volver</a>")

# 3. Vista para procesar el pedido
@login_required
def procesar_pedido(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        return HttpResponse("El carrito está vacío. No se puede procesar el pedido.", status=400)

    # Creamos el encabezado del pedido
    pedido = Pedido.objects.create(usuario=request.user, total=0)
    total_venta = 0

    for p_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=p_id)
        if producto.stock >= cantidad:
            producto.stock -= cantidad  # Restamos la cantidad del stock
            producto.save()             # Guardamos el cambio en la base de datos
        else:
            # Si no hay suficiente stock, podrías lanzar un error o saltar el producto
            return HttpResponse(f"No hay suficiente stock para {producto.nombre}", status=400)
        subtotal = producto.precio * cantidad
        total_venta += subtotal
        
        # Creamos el detalle
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )

    # Actualizamos el total y guardamos
    pedido.total = total_venta
    pedido.completado = True
    pedido.save()

    # Limpiamos el carrito de la sesión
    request.session['carrito'] = {}

    # Devolvemos una respuesta de éxito con HttpResponse
    return HttpResponse(f"<h1>Éxito</h1><p>Pedido #{producto.nombre} procesado por ${total_venta}.</p><a href='/ventas/productos'>Nueva venta</a>")