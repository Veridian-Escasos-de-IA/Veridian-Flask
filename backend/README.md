# 🏢 Sistema de Gestión del Edificio Multifuncional

API REST desarrollada con Flask para la gestión completa de un edificio multifuncional, incluyendo registro de usuarios, gestión de personas, departamentos y servicios.

## 🚀 Características

- **Autenticación JWT** - Sistema seguro de autenticación con tokens
- **Gestión de Personas** - CRUD completo para registro de personas
- **Base de Datos PostgreSQL** - Integración con esquema real de 42 tablas
- **Validación Robusta** - Esquemas de validación con Marshmallow
- **Documentación Automática** - Swagger/OpenAPI integrado
- **Arquitectura Limpia** - Estructura profesional y escalable

## 📁 Estructura del Proyecto

```
backend/
├── src/                          # Código fuente principal
│   ├── api/                      # Endpoints de la API
│   │   ├── personas.py          # CRUD de personas
│   │   └── __init__.py
│   ├── auth/                     # Sistema de autenticación
│   │   ├── auth.py              # Login, registro, JWT
│   │   └── __init__.py
│   ├── core/                     # Configuración central
│   │   ├── config.py            # Configuraciones del sistema
│   │   ├── database.py          # Configuración de DB y extensiones
│   │   └── __init__.py
│   ├── models/                   # Modelos SQLAlchemy
│   │   ├── models.py            # PersonaBase, User, Departamento, etc.
│   │   └── __init__.py
│   ├── schemas/                  # Esquemas de validación
│   │   ├── schemas.py           # Marshmallow schemas
│   │   └── __init__.py
│   ├── utils/                    # Utilidades
│   │   ├── responses.py         # Respuestas estándar de API
│   │   ├── decorators.py        # Decoradores de validación
│   │   └── __init__.py
│   ├── app.py                   # Factory de aplicación Flask
│   └── __init__.py
├── main.py                      # Punto de entrada principal
├── requirements.txt             # Dependencias Python
├── .env                        # Variables de entorno
└── README.md                  # Este archivo
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- PostgreSQL 12+
- Git

### Pasos de Instalación

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar PostgreSQL**
   - Crear base de datos llamada `Edificio`
   - Ajustar credenciales en `.env`

4. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

5. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:admin@127.0.0.1:5432/Edificio
JWT_SECRET_KEY=super-secret-jwt-key-for-development-only
CORS_ORIGINS=http://localhost:5173
```

## 🌐 API Endpoints

### Autenticación (`/api/auth`)

- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/refresh` - Renovar token
- `GET /api/auth/me` - Obtener perfil del usuario
- `POST /api/auth/logout` - Cerrar sesión

### Personas (`/api/personas`)

- `GET /api/personas/` - Listar personas (con paginación)
- `POST /api/personas/` - Crear nueva persona
- `GET /api/personas/<ci>` - Obtener persona por CI
- `PUT /api/personas/<ci>` - Actualizar persona
- `DELETE /api/personas/<ci>` - Eliminar persona (soft delete)

### Sistema

- `GET /` - Información general del sistema
- `GET /health` - Estado del sistema
- `GET /docs/` - Documentación Swagger

## 📚 Documentación API

La documentación completa de la API está disponible en:
- **Swagger UI**: `http://localhost:5000/docs/`

## 🔒 Autenticación

El sistema utiliza JWT (JSON Web Tokens):

1. **Registro/Login** → Recibe `access_token` y `refresh_token`
2. **Requests** → Incluir header: `Authorization: Bearer <access_token>`
3. **Renovación** → Usar `refresh_token` en `/api/auth/refresh`

## 🧪 Testing

### Verificar Estado del Sistema

```bash
curl http://localhost:5000/health
```

### Crear Usuario de Prueba

```python
import requests

data = {
    "ci": "12345678",
    "nombres": "Juan Carlos",
    "apellido_paterno": "Pérez",
    "fecha_nacimiento": "1990-05-15",
    "sexo": "M",
    "correo": "juan@test.com",
    "password": "password123",
    "password_confirm": "password123"
}

response = requests.post('http://localhost:5000/api/auth/register', json=data)
print(response.json())
```

## 🚀 Producción

```bash
# Instalar gunicorn
pip install gunicorn

# Ejecutar en producción
gunicorn -w 4 -b 0.0.0.0:5000 "src.app:create_app()"
```

---

**Versión**: 1.0.0  
**Sistema de Gestión del Edificio Multifuncional**