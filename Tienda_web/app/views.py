from django.shortcuts import render , get_object_or_404 , redirect 
from .models import Producto , Boleta , Detalle_boleta , Marca , Caracterista , Categoria
from django.http import JsonResponse 
import json

# Create your views here.

# Vista principal
def index(request ):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'app/index.html',data) 

# Vista del carrito
def carrito(request):
    order, created = Boleta.objects.get_or_create(cliente=request.user, completada=False)
    items = order.detalle_boleta_set.all()
    items_carrito = order.get_item  

    data = {
        'order': order, 
        'items': items,
        'items_carrito': items_carrito,
    }
    return render(request, 'app/carrito.html', data)

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    order, created = Boleta.objects.get_or_create(cliente=1, completada=False)
    detalle_orden, created = Detalle_boleta.objects.get_or_create(boleta=order, producto=producto)
    detalle_orden.cantidad_productos += 1
    detalle_orden.save()
    return redirect('carrito')


def quitar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    order = Boleta.objects.get(cliente=1, completada=False)
    detalle_orden = Detalle_boleta.objects.get(boleta=order, producto=producto)
    if detalle_orden.cantidad_productos > 1:
        detalle_orden.cantidad_productos -= 1
        detalle_orden.save()
    else:
        detalle_orden.delete()
    return redirect('carrito')


def ver_carrito(request):
    order = Boleta.objects.filter(cliente=1, completada=False).first()
    context = {
        'order': order
    }
    return render(request, 'carrito.html', context)

# funcion Para actualizar los cambias del carrito
def actualizarCarrito(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    producto = Producto.objects.get(id=productId)
    order,creada = Boleta.objects.get_or_create(cliente=1,completada=False)
    detalle_orden,creada = Detalle_boleta.objects.get_or_create(boleta=order,producto=producto)
    if action == 'add':
        if detalle_orden.cantidad_productos < producto.stock: 
            detalle_orden.cantidad_productos +=1
    elif action == 'remove': 
        detalle_orden.cantidad_productos -=1
    
    elif action == 'delete':
        detalle_orden.cantidad_productos = 0    
    detalle_orden.save()          
    if detalle_orden.cantidad_productos <= 0: 
        detalle_orden.delete()
    return JsonResponse("Carrito actualizado",safe=False) 

# vista del detalle del producto
def detalle_producto(request,id):
    producto=get_object_or_404(Producto,id=id)
    producto1=get_object_or_404(Producto,id=2)
    producto2=get_object_or_404(Producto,id=3)
    producto3=get_object_or_404(Producto,id=4)
    datos = {

        "producto":producto,
        "producto1": producto1,
        "producto2": producto2,
        "producto3":producto3
    }
    return render(request, 'app/detalle_producto.html',datos )

# Vista para la busqueda de productos por filtro
def filtro(request):
    query = request.GET.get('q')
    marca_id = request.GET.get('marca')
    min_precio = request.GET.get('min_precio')
    max_precio = request.GET.get('max_precio')

    productos = Producto.objects.all()
   

    if query:
        productos = productos.filter(nombre__icontains=query)
    elif marca_id:
        productos = productos.filter(marca_id=marca_id)

    if min_precio:
        productos = productos.filter(precio__gte=min_precio)

    if max_precio:
        productos = productos.filter(precio__lte=max_precio)
    
    categorias = Categoria.objects.all()
    
    categoria_id = request.GET.get('categoria', '')
    if categoria_id.isdigit():
        productos = productos.filter(categoria_id=categoria_id)

    # Filtrar por color
    color = request.GET.get('color', '')
    if color:
        productos = productos.filter(caracterista__color=color)

    # Filtrar por material
    material = request.GET.get('material', '')
    if material:
        productos = productos.filter(caracterista__material=material)

    # Filtrar por bluetooth
    bluetooth = request.GET.get('bluetooth', '')
    if bluetooth:
        productos = productos.filter(caracterista__bluetooth=bluetooth)

    marcas = Marca.objects.all()

    context = {
        'productos': productos,
        'marcas': marcas,
        'categorias': categorias
    }
    return render(request, 'app/filtro.html', context)


