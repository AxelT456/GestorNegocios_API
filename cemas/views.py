from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import ProtectedError

from django.db import transaction # Importante para que la venta sea segura
from .models import MovimientoFinanciero, Venta, DetalleVenta
from .serializers import MovimientoFinancieroSerializer, VentaSerializer

from .models import Categoria, Producto
from .serializers import (
    RegistroUsuarioSerializer, LoginSerializer, 
    CategoriaSerializer, ProductoSerializer
)

# =========================================================
# 1. AUTENTICACIÓN (Registro, Login, Logout)
# =========================================================

class RegistroView(APIView):
    permission_classes = [permissions.AllowAny] # Público

    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.pk,
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny] # Público

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "token": token.key,
                    "user_id": user.pk,
                    "username": user.username
                })
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Privado

    def post(self, request):
        # Borra el token del usuario actual
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# =========================================================
# 2. CRUD DE CATEGORÍAS
# =========================================================

class CategoriaListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # SOLO devuelve categorías creadas por el usuario logueado
        categorias = Categoria.objects.filter(usuario=request.user)
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            # Asigna automáticamente el usuario logueado
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, usuario):
        obj = get_object_or_404(Categoria, pk=pk)
        if obj.usuario != usuario:
            return None # No es tuyo
        return obj

    def put(self, request, pk):
        categoria = self.get_object(pk, request.user)
        if not categoria:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categoria = self.get_object(pk, request.user)
        if not categoria:
            return Response(status=status.HTTP_403_FORBIDDEN)
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =========================================================
# 3. CRUD DE PRODUCTOS
# =========================================================

class ProductoListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        productos = Producto.objects.filter(usuario=request.user)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, usuario):
        obj = get_object_or_404(Producto, pk=pk)
        if obj.usuario != usuario:
            return None
        return obj

    def get(self, request, pk):
        producto = self.get_object(pk, request.user)
        if not producto:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    def put(self, request, pk):
        producto = self.get_object(pk, request.user)
        if not producto:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        producto = self.get_object(pk, request.user)
        if not producto:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        try:
            producto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {"error": "No puedes eliminar este producto porque ya tiene ventas registradas."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
# =========================================================
# 4. CRUD DE MOVIMIENTOS FINANCIEROS (Gastos / Ingresos Extra)
# =========================================================

class MovimientoListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Filtramos por fecha si queremos, pero por ahora devolvemos todo lo del usuario
        movimientos = MovimientoFinanciero.objects.filter(usuario=request.user).order_by('-fecha')
        serializer = MovimientoFinancieroSerializer(movimientos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovimientoFinancieroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovimientoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        movimiento = get_object_or_404(MovimientoFinanciero, pk=pk, usuario=request.user)
        movimiento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =========================================================
# 5. PROCESAR VENTA (La Lógica Maestra)
# =========================================================

class ProcesarVentaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Datos esperados:
        # {
        #   "metodo_pago": "EFECTIVO",
        #   "productos": [
        #       {"id": 1, "cantidad": 2},
        #       {"id": 5, "cantidad": 1}
        #   ]
        # }
        
        datos = request.data
        productos_solicitados = datos.get('productos', [])
        metodo_pago = datos.get('metodo_pago', 'EFECTIVO')

        if not productos_solicitados:
            return Response({"error": "La venta debe tener al menos un producto"}, status=status.HTTP_400_BAD_REQUEST)

        # Usamos transaction.atomic para asegurar que si algo falla, no se guarde nada a medias
        with transaction.atomic():
            # 1. Crear la Venta (Cabecera)
            nueva_venta = Venta.objects.create(
                usuario=request.user,
                total=0, # Lo calcularemos ahorita
                metodo_pago=metodo_pago
            )

            total_acumulado = 0

            # 2. Recorrer cada producto solicitado
            for item in productos_solicitados:
                producto_id = item.get('id')
                cantidad = item.get('cantidad')

                # Buscar producto y validar que sea de ESTE usuario
                producto = get_object_or_404(Producto, pk=producto_id, usuario=request.user)
                
                # Calcular precio al momento de la venta
                precio_final = producto.precio_venta
                subtotal = precio_final * cantidad
                
                # Crear el detalle
                DetalleVenta.objects.create(
                    venta=nueva_venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_final,
                    subtotal=subtotal
                )

                total_acumulado += subtotal

            # 3. Actualizar el total final de la venta
            nueva_venta.total = total_acumulado
            nueva_venta.save()

            # Devolvemos la venta completa con sus detalles
            serializer = VentaSerializer(nueva_venta)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class HistorialVentasView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Traer todas las ventas del usuario ordenadas por fecha (la más reciente primero)
        ventas = Venta.objects.filter(usuario=request.user).order_by('-fecha')
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data)