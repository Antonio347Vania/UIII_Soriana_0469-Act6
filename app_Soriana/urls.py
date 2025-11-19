from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Departamentos
    path('departamentos/', views.inicio_Departamento, name='inicio_Departamento'),
    path('departamentos/agregar/', views.agregar_Departamento, name='agregar_Departamento'),
    path('departamentos/actualizar/<int:id>/', views.actualizar_Departamento, name='actualizar_Departamento'),
    path('departamentos/actualizar/realizar/<int:id>/', views.realizar_actualizacion_Departamento, name='realizar_actualizacion_Departamento'),
    path('departamentos/borrar/<int:id>/', views.borrar_Departamento, name='borrar_Departamento'),

    # Empleados
    path('empleados/', views.inicio_Empleados, name='inicio_Empleados'),
    path('empleados/agregar/', views.agregar_Empleados, name='agregar_Empleados'),
    path('empleados/actualizar/<int:id>/', views.actualizar_Empleados, name='actualizar_Empleados'),
    path('empleados/actualizar/realizar/<int:id>/', views.realizar_actualizacion_Empleados, name='realizar_actualizacion_Empleados'),
    path('empleados/borrar/<int:id>/', views.borrar_Empleados, name='borrar_Empleados'),

    # Clientes
    path('clientes/', views.inicio_Clientes, name='inicio_Clientes'),
    path('clientes/agregar/', views.agregar_Clientes, name='agregar_Clientes'),
    path('clientes/actualizar/<int:id>/', views.actualizar_Clientes, name='actualizar_Clientes'),
    path('clientes/actualizar/realizar/<int:id>/', views.realizar_actualizacion_Clientes, name='realizar_actualizacion_Clientes'),
    path('clientes/borrar/<int:id>/', views.borrar_Clientes, name='borrar_Clientes'),

    # Productos
    path('productos/', views.inicio_Productos, name='inicio_Productos'),
    path('productos/agregar/', views.agregar_Productos, name='agregar_Productos'),
    path('productos/actualizar/<int:id>/', views.actualizar_Productos, name='actualizar_Productos'),
    path('productos/actualizar/realizar/<int:id>/', views.realizar_actualizacion_Productos, name='realizar_actualizacion_Productos'),
    path('productos/borrar/<int:id>/', views.borrar_Productos, name='borrar_Productos'),

    # Pedidos
    path('pedidos/', views.inicio_Pedidos, name='inicio_Pedidos'),
    path('pedidos/agregar/', views.agregar_Pedidos, name='agregar_Pedidos'),
    path('pedidos/actualizar/<int:id>/', views.actualizar_Pedidos, name='actualizar_Pedidos'),
    path('pedidos/actualizar/realizar/<int:id>/', views.realizar_actualizacion_Pedidos, name='realizar_actualizacion_Pedidos'),
    path('pedidos/borrar/<int:id>/', views.borrar_Pedidos, name='borrar_Pedidos'),

    # Ventas
    path('ventas/', views.inicio_Ventas, name='inicio_Ventas'),
    path('ventas/agregar/', views.agregar_Ventas, name='agregar_Ventas'),
    path('ventas/actualizar/<int:id>/', views.actualizar_Ventas, name='actualizar_Ventas'),
    path('ventas/actualizar/realizar/<int:id>/', views.realizar_actualizacion_Ventas, name='realizar_actualizacion_Ventas'),
    path('ventas/borrar/<int:id>/', views.borrar_Ventas, name='borrar_Ventas'),
]