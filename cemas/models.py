from django.db import models
from django.contrib.auth.models import User

# 1. CATEGORÍAS (Para análisis de gráficas)
class Categoria(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('GASTO', 'Gasto'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Seguridad: Cada negocio sus categorias
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

# 2. PRODUCTOS (Lo que vendes)
# Aunque es financiero, necesitas saber qué vendes para cobrar.
class Producto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    # Opcional: costo_produccion para calcular ganancia neta real por producto
    costo_aprox = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.nombre

# 3. TRANSACCIONES (El núcleo del flujo de caja)
class MovimientoFinanciero(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=255)
    es_gasto = models.BooleanField(default=True) # True = Salida de dinero, False = Entrada extra
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        signo = "-" if self.es_gasto else "+"
        return f"{signo}${self.monto} - {self.descripcion}"

class Venta(models.Model):
    # Definimos las opciones fijas (tupla: valor_db, valor_humano)
    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Campo nuevo:
    metodo_pago = models.CharField(
        max_length=20, 
        choices=METODOS_PAGO, 
        default='EFECTIVO'
    )
    
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta #{self.id} - ${self.total} ({self.metodo_pago})"

# 5. DETALLE DE VENTA
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT) # Si borras el producto, el historial queda
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Se guarda el precio del momento
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)