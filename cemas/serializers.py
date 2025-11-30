from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Categoria, Producto, MovimientoFinanciero, Venta, DetalleVenta

# =========================================================
# 1. AUTH SERIALIZERS
# =========================================================

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# =========================================================
# 2. CATALOGOS (Categorias y Productos)
# =========================================================

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        read_only_fields = ('usuario',)
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        read_only_fields = ('usuario',)
        fields = '__all__'


# =========================================================
# 3. FINANZAS (ESTO ES LO QUE TE FALTABA)
# =========================================================

class MovimientoFinancieroSerializer(serializers.ModelSerializer):
    # Agregamos el nombre de la categoría para leerlo fácil en el frontend
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = MovimientoFinanciero
        # Usuario y fecha se llenan solos, no los pedimos
        read_only_fields = ('usuario', 'fecha')
        fields = ['id', 'monto', 'descripcion', 'es_gasto', 'fecha', 'categoria', 'categoria_nombre']

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal']

class VentaSerializer(serializers.ModelSerializer):
    # Incluimos los detalles anidados (Nested Serializer)
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        read_only_fields = ('usuario', 'fecha', 'total')
        fields = ['id', 'total', 'metodo_pago', 'fecha', 'detalles']