from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_datetime, parse_date
from django.db.models import DateField, DateTimeField
from .models import Departamento, Productos, Empleados, Clientes, Pedidos, Ventas
from django.db.models import ProtectedError

import re

def inicio(request):
    return render(request, 'inicio.html')

# ================= DEPARTAMENTOS =================
def inicio_Departamento(request):
    departamentos = Departamento.objects.all()
    return render(request, 'Departamentos/ver_Departamentos.html', {'departamentos': departamentos})

def agregar_Departamento(request):
    if request.method == 'POST':
        Departamento.objects.create(
            nombre_departamento=request.POST['nombre'],
            descripcion=request.POST['descripcion']
        )
        return redirect('inicio_Departamento')
    return render(request, 'Departamentos/agregar_Departamento.html')

def actualizar_Departamento(request, id):
    departamento = get_object_or_404(Departamento, id=id)
    return render(request, 'Departamentos/actualizar_Departamento.html', {'departamento': departamento})

def realizar_actualizacion_Departamento(request, id):
    if request.method == 'POST':
        d = get_object_or_404(Departamento, id=id)
        d.nombre_departamento = request.POST['nombre']
        d.descripcion = request.POST['descripcion']
        d.save()
    return redirect('inicio_Departamento')

def borrar_Departamento(request, id):
    departamento = get_object_or_404(Departamento, pk=id)
    if request.method == 'POST':
        departamento.delete()
        messages.success(request, 'Departamento eliminado correctamente.')
        return redirect('inicio_Departamento')
    return render(request, 'Departamentos/borrar_departamento.html', {'departamento': departamento})

# ================= EMPLEADOS =================
def inicio_Empleados(request):
    empleados = Empleados.objects.all()
    return render(request, 'Empleados/ver_Empleados.html', {'empleados': empleados})

def agregar_Empleados(request):
    if request.method == 'POST':
        Empleados.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            puesto=request.POST['puesto'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            salario=request.POST['salario']
        )
        return redirect('inicio_Empleados')
    return render(request, 'Empleados/agregar_Empleados.html')

def actualizar_Empleados(request, id):
    empleado = get_object_or_404(Empleados, id=id)
    return render(request, 'Empleados/actualizar_Empleados.html', {'empleado': empleado})

def realizar_actualizacion_Empleados(request, id):
    if request.method == 'POST':
        e = get_object_or_404(Empleados, id=id)
        e.nombre = request.POST['nombre']
        e.apellido = request.POST['apellido']
        e.puesto = request.POST['puesto']
        e.fecha_contratacion = request.POST['fecha_contratacion']
        e.salario = request.POST['salario']
        e.save()
    return redirect('inicio_Empleados')

def borrar_Empleados(request, id):
    empleado = get_object_or_404(Empleados, id=id)
    
    if request.method == 'POST':
        try:
            empleado.delete()
            messages.success(request, 'Empleado eliminado correctamente.')
            return redirect('inicio_Empleados')
        
        except ProtectedError:
            # Esto pasa si el empleado tiene ventas o pedidos registrados
            messages.error(request, 'No se puede eliminar este empleado porque tiene Ventas o Pedidos asociados.')
        
        except Exception as e:
            messages.error(request, f'Error desconocido al eliminar: {str(e)}')

    return render(request, 'Empleados/borrar_empleado.html', {'empleado': empleado})
# ================= CLIENTES =================
def inicio_Clientes(request):
    clientes = Clientes.objects.all()
    return render(request, 'Clientes/ver_Clientes.html', {'clientes': clientes})

def agregar_Clientes(request):
    if request.method == 'POST':
        Clientes.objects.create(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            email=request.POST['email'],
            telefono=request.POST['telefono'],
            tipo_registro=request.POST['tipo_registro']
        )
        return redirect('inicio_Clientes')
    return render(request, 'Clientes/agregar_Clientes.html')

def actualizar_Clientes(request, id):
    cliente = get_object_or_404(Clientes, id=id)
    return render(request, 'Clientes/actualizar_Clientes.html', {'cliente': cliente})

def realizar_actualizacion_Clientes(request, id):
    if request.method == 'POST':
        c = get_object_or_404(Clientes, id=id)
        c.nombre = request.POST['nombre']
        c.apellido = request.POST['apellido']
        c.email = request.POST['email']
        c.telefono = request.POST['telefono']
        c.tipo_registro = request.POST['tipo_registro']
        c.save()
    return redirect('inicio_Clientes')

def borrar_Clientes(request, id):
    cliente = get_object_or_404(Clientes, id=id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('inicio_Clientes')
    return render(request, 'Clientes/borrar_cliente.html', {'cliente': cliente})

# ================= PRODUCTOS =================
def inicio_Productos(request):
    productos = Productos.objects.all()
    return render(request, 'Productos/ver_Productos.html', {'productos': productos})

def agregar_Productos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_producto', '').strip()
        precio_raw = request.POST.get('precio', '').strip()
        
        # Correcto: busca 'stock' como se llama en el HTML
        stock_raw = request.POST.get('stock', '').strip()
        
        depto_id = request.POST.get('id_departamento', '')
        imagen = request.FILES.get('imagen')

        if not nombre:
            messages.error(request, 'El nombre del producto es obligatorio.')
            departamentos = Departamento.objects.all()
            return render(request, 'Productos/agregar_Productos.html', {'departamentos': departamentos})

        # Precio: usar Decimal seguro
        try:
            precio = Decimal(precio_raw) if precio_raw != '' else Decimal('0.00')
        except (InvalidOperation, TypeError):
            messages.error(request, 'Precio inválido.')
            departamentos = Departamento.objects.all()
            return render(request, 'Productos/agregar_Productos.html', {'departamentos': departamentos})

        # STOCK: parsing tolerante
        stock = 0
        if stock_raw != '':
            s = stock_raw.strip()
            s = s.replace(' ', '')
            if ',' in s and '.' in s:
                s = s.replace(',', '')
            elif ',' in s and '.' not in s:
                s = s.replace(',', '.')
            s = re.sub(r'[^0-9\.-]', '', s)
            try:
                stock_val = float(s)
                stock = int(stock_val)
                if stock < 0:
                    stock = 0
            except Exception:
                stock = 0
                messages.warning(request, f'Valor de stock inválido ("{stock_raw}"), se usará 0 por defecto.')

        # Departamento
        departamento = None
        if depto_id:
            try:
                departamento = Departamento.objects.get(pk=int(depto_id))
            except (Departamento.DoesNotExist, ValueError):
                departamento = None

        producto = Productos(
            nombre_producto=nombre,
            precio=precio,
            stock_disponible=stock,
            id_departamento=departamento,
            imagen=imagen
        )
        producto.save()
        messages.success(request, 'Producto creado correctamente.')
        return redirect('inicio_Productos')

    departamentos = Departamento.objects.all()
    return render(request, 'Productos/agregar_Productos.html', {'departamentos': departamentos})

def actualizar_Productos(request, id):
    producto = get_object_or_404(Productos, pk=id)
    # Esta vista es solo para GET (mostrar el formulario), la logica POST está en realizar_actualizacion_Productos
    # aunque si decidieras manejar POST aquí, necesitarías la corrección también.
    # Por seguridad, dejo la logica POST aquí tambien corregida por si la URL apunta aquí en algun momento.
    if request.method == 'POST':
        nombre = request.POST.get('nombre_producto', '').strip()
        precio_raw = request.POST.get('precio', '').strip()
        stock_raw = request.POST.get('stock', '').strip() # CORREGIDO
        descripcion = request.POST.get('descripcion', '').strip()
        depto_id = request.POST.get('id_departamento', '')
        imagen = request.FILES.get('imagen')

        try:
            precio = float(precio_raw)
        except (ValueError, TypeError):
            precio = producto.precio
        try:
            stock = int(stock_raw)
        except (ValueError, TypeError):
            stock = producto.stock_disponible

        producto.nombre_producto = nombre or producto.nombre_producto
        producto.precio = precio
        producto.stock_disponible = stock
        producto.descripcion = descripcion or producto.descripcion

        if depto_id:
            try:
                producto.id_departamento = Departamento.objects.get(pk=int(depto_id))
            except (Departamento.DoesNotExist, ValueError):
                pass

        if imagen:
            producto.imagen = imagen

        producto.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('inicio_Productos')

    departamentos = Departamento.objects.all()
    return render(request, 'Productos/actualizar_producto.html', {'producto': producto, 'departamentos': departamentos})

def realizar_actualizacion_Productos(request, id):
    producto = get_object_or_404(Productos, pk=id)
    if request.method == 'POST':
        # Campos simples
        nombre = request.POST.get('nombre_producto', '').strip()
        precio_raw = request.POST.get('precio', '').strip()
        
        # --- CORRECCIÓN REALIZADA AQUÍ ---
        # Antes buscabas 'stock_disponible', pero tu input HTML se llama 'stock'
        stock_raw = request.POST.get('stock', '').strip()
        # ---------------------------------
        
        descripcion = request.POST.get('descripcion', '').strip()
        depto_id = request.POST.get('id_departamento', '')

        # Validar/convertir precio
        try:
            precio = Decimal(precio_raw) if precio_raw != '' else producto.precio
        except InvalidOperation:
            messages.error(request, 'Precio inválido.')
            departamentos = Departamento.objects.all()
            return render(request, 'Productos/actualizar_producto.html', {'producto': producto, 'departamentos': departamentos})

        # Convertir stock
        try:
            # Si viene vacío, mantiene el valor anterior (producto.stock_disponible)
            # Si viene valor, lo convierte a int.
            if stock_raw != '':
                 # Usamos float intermedio por si envían algo como "10.0"
                stock = int(float(stock_raw))
            else:
                stock = producto.stock_disponible
        except ValueError:
            # Si falla la conversión, mantiene el anterior
            stock = producto.stock_disponible

        # Asignaciones básicas
        producto.nombre_producto = nombre or producto.nombre_producto
        producto.precio = precio
        producto.stock_disponible = stock
        producto.descripcion = descripcion or producto.descripcion

        if depto_id:
            try:
                producto.id_departamento = Departamento.objects.get(pk=int(depto_id))
            except (Departamento.DoesNotExist, ValueError):
                pass

        # Imagen: solo reemplazar si hay archivo nuevo
        imagen = request.FILES.get('imagen')
        if imagen:
            producto.imagen = imagen

        # Manejo genérico de campos DateField/DateTimeField del modelo
        for field in producto._meta.fields:
            if isinstance(field, (DateField, DateTimeField)):
                post_val = request.POST.get(field.name, None)
                if post_val is None:
                    continue
                post_val = post_val.strip()
                if post_val == '':
                    if field.null:
                        setattr(producto, field.name, None)
                else:
                    normalized = post_val.replace('T', ' ')
                    if isinstance(field, DateTimeField):
                        parsed = parse_datetime(normalized)
                    else:
                        parsed = parse_date(normalized)
                    if parsed:
                        setattr(producto, field.name, parsed)
                    else:
                        messages.error(request, f'Formato inválido para {field.name}.')
                        departamentos = Departamento.objects.all()
                        return render(request, 'Productos/actualizar_producto.html', {'producto': producto, 'departamentos': departamentos})

        producto.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('inicio_Productos')

    departamentos = Departamento.objects.all()
    return render(request, 'Productos/actualizar_producto.html', {'producto': producto, 'departamentos': departamentos})

def borrar_Productos(request, id):
    producto = get_object_or_404(Productos, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('inicio_Productos')
    return render(request, 'Productos/borrar_producto.html', {'producto': producto})

# ================= PEDIDOS =================
def inicio_Pedidos(request):
    pedidos = Pedidos.objects.all()
    return render(request, 'Pedidos/ver_Pedidos.html', {'pedidos': pedidos})

def agregar_Pedidos(request):
    clientes = Clientes.objects.all()
    empleados = Empleados.objects.all()
    if request.method == 'POST':
        cliente = Clientes.objects.get(id=request.POST['id_cliente'])
        empleado = Empleados.objects.get(id=request.POST['id_empleado']) if request.POST.get('id_empleado') else None
        Pedidos.objects.create(
            id_cliente=cliente,
            id_empleado=empleado,
            estado_pedido=request.POST['estado'],
            cant_productos=request.POST['cant_productos'],
            total_pedido=request.POST['total'],
            metodo_pago=request.POST['metodo_pago']
        )
        return redirect('inicio_Pedidos')
    return render(request, 'Pedidos/agregar_Pedidos.html', {'clientes': clientes, 'empleados': empleados})

def actualizar_Pedidos(request, id):
    pedido = get_object_or_404(Pedidos, id=id)
    clientes = Clientes.objects.all()
    empleados = Empleados.objects.all()
    return render(request, 'Pedidos/actualizar_Pedidos.html', {'pedido': pedido, 'clientes': clientes, 'empleados': empleados})

def realizar_actualizacion_Pedidos(request, id):
    if request.method == 'POST':
        p = get_object_or_404(Pedidos, id=id)
        p.id_cliente = Clientes.objects.get(id=request.POST['id_cliente'])
        p.id_empleado = Empleados.objects.get(id=request.POST['id_empleado']) if request.POST.get('id_empleado') else None
        p.estado_pedido = request.POST['estado']
        p.cant_productos = request.POST['cant_productos']
        p.total_pedido = request.POST['total']
        p.metodo_pago = request.POST['metodo_pago']
        p.save()
    return redirect('inicio_Pedidos')

def borrar_Pedidos(request, id):
    pedido = get_object_or_404(Pedidos, id=id)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido eliminado correctamente.')
        return redirect('inicio_Pedidos')
    return render(request, 'Pedidos/borrar_pedido.html', {'pedido': pedido})

# ================= VENTAS =================
def inicio_Ventas(request):
    ventas = Ventas.objects.all()
    return render(request, 'Ventas/ver_Ventas.html', {'ventas': ventas})

def agregar_Ventas(request):
    clientes = Clientes.objects.all()
    empleados = Empleados.objects.all()
    if request.method == 'POST':
        cliente = Clientes.objects.get(id=request.POST['id_cliente'])
        empleado = Empleados.objects.get(id=request.POST['id_empleado'])
        Ventas.objects.create(
            id_cliente=cliente,
            id_empleado=empleado,
            cant_productos=request.POST['cant_productos'],
            total_venta=request.POST['total'],
            metodo_pago=request.POST['metodo_pago']
        )
        return redirect('inicio_Ventas')
    return render(request, 'Ventas/agregar_Ventas.html', {'clientes': clientes, 'empleados': empleados})

def actualizar_Ventas(request, id):
    venta = get_object_or_404(Ventas, id=id)
    clientes = Clientes.objects.all()
    empleados = Empleados.objects.all()
    return render(request, 'Ventas/actualizar_Ventas.html', {'venta': venta, 'clientes': clientes, 'empleados': empleados})

def realizar_actualizacion_Ventas(request, id):
    if request.method == 'POST':
        v = get_object_or_404(Ventas, id=id)
        v.id_cliente = Clientes.objects.get(id=request.POST['id_cliente'])
        v.id_empleado = Empleados.objects.get(id=request.POST['id_empleado'])
        v.cant_productos = request.POST['cant_productos']
        v.total_venta = request.POST['total']
        v.metodo_pago = request.POST['metodo_pago']
        v.save()
    return redirect('inicio_Ventas')

def borrar_Ventas(request, id):
    venta = get_object_or_404(Ventas, id=id)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada correctamente.')
        return redirect('inicio_Ventas')
    return render(request, 'Ventas/borrar_venta.html', {'venta': venta})