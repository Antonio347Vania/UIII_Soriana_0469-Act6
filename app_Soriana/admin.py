from django.contrib import admin
from .models import Departamento, Productos, Empleados, Clientes, Pedidos, Ventas

admin.site.register(Departamento)
admin.site.register(Productos)
admin.site.register(Empleados)
admin.site.register(Clientes)
admin.site.register(Pedidos)
admin.site.register(Ventas)