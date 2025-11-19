from django.db import models

# ==========================================
# MODELO : Departamento
# ==========================================
class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_departamento

# ==========================================
# MODELO : Empleados
# ==========================================
class Empleados(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ==========================================
# MODELO : Clientes
# ==========================================
class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    TIPO_REGISTRO_CHOICES = [
        ('Local', 'Local'),
        ('En linea', 'En linea'),
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    tipo_registro = models.CharField(max_length=20, choices=TIPO_REGISTRO_CHOICES, default='Particular')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ==========================================
# MODELO : Productos
# ==========================================
class Productos(models.Model):
    id = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    nombre_producto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    stock_disponible = models.IntegerField(default=0)
    fecha_caducidad = models.DateTimeField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre_producto

# ==========================================
# MODELO : Pedidos
# ==========================================
class Pedidos(models.Model):
    id = models.AutoField(primary_key=True)
    ESTADO_PEDIDO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Procesando', 'Procesando'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]
    METODO_PAGO_CHOICES = [
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia Bancaria'),
        ('PayPal', 'PayPal'),
    ]
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, blank=True, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=20, choices=ESTADO_PEDIDO_CHOICES, default='Pendiente')
    cant_productos = models.IntegerField(default=0)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, default='Tarjeta')

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.id_cliente.nombre}"

# ==========================================
# MODELO : Ventas
# ==========================================
class Ventas(models.Model):
    id = models.AutoField(primary_key=True)
    METODO_PAGO_CHOICES = [
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia Bancaria'),
        ('PayPal', 'PayPal'),
    ]
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    cant_productos = models.IntegerField(default=0)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, default='Tarjeta')

    def __str__(self):
        return f"Venta {self.id}"