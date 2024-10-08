from django.urls import path
from .views import index , carrito , agregar_al_carrito , quitar_del_carrito , actualizarCarrito  , filtro , detalle_producto

# Url de mi pagina 
urlpatterns = [
    path('', index , name="index"),
    path('filtro/', filtro , name="filtro"),
    path('detalle_producto/<id>/', detalle_producto , name="detalle_producto"),
    path('carrito/', carrito , name="carrito"),
    path('actualizar_carrito/', actualizarCarrito, name='actualizar_carrito'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar-del-carrito/<int:producto_id>/', quitar_del_carrito, name='quitar_del_carrito'),
]

