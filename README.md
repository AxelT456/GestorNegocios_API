# 🍔 API Gestor de Negocios (CEMAS)

Backend desarrollado en Django para la administración financiera y operativa de micro-negocios gastronómicos. Este sistema permite gestionar inventarios, registrar ventas en tiempo real y analizar el flujo de caja (ingresos vs gastos) en una arquitectura Multi-tenant (SaaS).

## 🚀 Tecnologías

* **Lenguaje:** Python 3.x
* **Framework:** Django 4.2 LTS
* **API:** Django REST Framework (DRF)
* **Base de Datos:** MySQL / MariaDB (XAMPP)
* **Seguridad:** Token Authentication (DRF Auth Token)

## 📋 Prerrequisitos

* Python 3.10 o superior
* Servidor MySQL corriendo (XAMPP, WAMP o Docker)
* Git

## 🔧 Instalación y Configuración

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/AxelT456/GestorNegocios_API.git](https://github.com/AxelT456/GestorNegocios_API.git)
    cd GestorNegocios_API
    ```

2.  **Crear y activar entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuración de Base de Datos:**
    * Asegúrate de tener una base de datos vacía en MySQL llamada `db_finanzas` (o ajusta el nombre en `core/settings.py`).
    * Configura tu usuario y contraseña de MySQL en `settings.py`.

5.  **Migraciones:**
    ```bash
    python manage.py migrate
    ```

6.  **Crear Superusuario (Admin):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecutar servidor:**
    ```bash
    python manage.py runserver
    ```

## 📡 Documentación de Endpoints (API)

Todas las peticiones (excepto Auth) requieren el Header:
`Authorization: Token <tu_token>`

### Autenticación
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/auth/registro/` | Registrar nuevo negocio/usuario |
| `POST` | `/api/auth/login/` | Iniciar sesión y obtener Token |
| `POST` | `/api/auth/logout/` | Cerrar sesión (Invalidar Token) |

### Inventario
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET/POST` | `/api/categorias/` | Gestionar categorías |
| `GET/POST` | `/api/productos/` | Gestionar catálogo de productos |
| `PUT/DEL` | `/api/productos/<id>/` | Editar o eliminar producto |

### Finanzas y Operación
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/ventas/nueva/` | Registrar una venta compleja (Múltiples productos) |
| `GET` | `/api/ventas/historial/` | Ver historial de ventas |
| `POST` | `/api/movimientos/` | Registrar gastos o ingresos extra (Caja chica) |