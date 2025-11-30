from django.urls import path
from .views import (
    RegistroView, LoginView, LogoutView,
    CategoriaListCreateView, CategoriaDetailView,
    ProductoListCreateView, ProductoDetailView,
    MovimientoListCreateView, MovimientoDetailView,
    ProcesarVentaView, HistorialVentasView
)

urlpatterns = [
    # --- AUTENTICACIÓN ---
    path('auth/registro/', RegistroView.as_view(), name='registro'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # --- CATEGORÍAS ---
    path('categorias/', CategoriaListCreateView.as_view()),
    path('categorias/<int:pk>/', CategoriaDetailView.as_view()),

    # --- PRODUCTOS ---
    path('productos/', ProductoListCreateView.as_view()),
    path('productos/<int:pk>/', ProductoDetailView.as_view()),

    # Gastos e Ingresos Manuales
    path('movimientos/', MovimientoListCreateView.as_view()), 
    path('movimientos/<int:pk>/', MovimientoDetailView.as_view()),

    # Ventas (Cajero)
    path('ventas/nueva/', ProcesarVentaView.as_view()),     # POST: Registrar venta
    path('ventas/historial/', HistorialVentasView.as_view()), # GET: Ver ventas
]