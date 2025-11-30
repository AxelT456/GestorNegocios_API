from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Categoria, Producto, MovimientoFinanciero, Venta, DetalleVenta

# --- AUTH SERIALIZERS ---
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

# --- MODEL SERIALIZERS ---
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