"""
Aplicación principal del Sistema de Gestión del Edificio Multifuncional
"""

import os
from flask import Flask, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def create_app(config_name: str = 'development'):
    """
    Crear y configurar la aplicación Flask

    Args:
        config_name: 'development' | 'production' | 'testing'
    """
    app = Flask(__name__)

    # -------- Configuración --------
    # Ejemplo: app/core/config.py define un dict 'config' con claves por entorno
    from app.core.config import config
    if config_name not in config:
        # fallback seguro si llega 'default'
        config_name = 'development'
    app.config.from_object(config[config_name])

    # -------- Extensiones / DB --------
    # Ejemplo: app/core/database.py expone init_extensions(app) y db
    from app.core.database import init_extensions
    init_extensions(app)

    # -------- Blueprints --------
    register_blueprints(app)

    # -------- Errores --------
    register_error_handlers(app)

    # -------- DB init (opcional si usas migraciones) --------
    try:
        from app.core.database import db
        with app.app_context():
            db.create_all()
            print("Base de datos inicializada")
    except Exception as e:
        # No fallar el arranque por esto si usas Alembic/Flask-Migrate
        print(f"Advertencia: no se pudo inicializar la base de datos: {e}")

    return app


def register_blueprints(app: Flask) -> None:
    """Registrar todos los blueprints de la aplicación"""

    # Personas API
    # Estructura esperada: app/blueprints/api/personas.py -> personas_bp
    from app.blueprints.api.personas import personas_bp
    app.register_blueprint(personas_bp)

    # Auth API
    # Estructura esperada: app/blueprints/auth/routes.py -> auth_bp, init_oauth
    from app.blueprints.auth.auth import auth_bp, init_oauth  # si init_oauth existe
# o, si tu __init__.py ya expone auth_bp/init_oauth:
# from app.blueprints.auth import auth_bp, init_oauth

    app.register_blueprint(auth_bp)

    # Inicializar OAuth (si aplica)
    init_oauth(app)

    # Salud del sistema
    @app.get('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Sistema de Gestión del Edificio Multifuncional',
            'version': '1.0.0'
        })

    # Ruta raíz
    @app.get('/')
    def index():
        return jsonify({
            'message': 'Sistema de Gestión del Edificio Multifuncional API',
            'version': '1.0.0',
            'documentation': '/docs/',
            'health': '/health',
            'endpoints': {
                'auth': '/api/auth/',
                'personas': '/api/personas/'
            }
        })


def register_error_handlers(app: Flask) -> None:
    """Registrar manejadores de errores globales"""

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint no encontrado',
            'error': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Método HTTP no permitido para este endpoint',
            'error': 'Method Not Allowed'
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Solicitud malformada',
            'error': 'Bad Request'
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor',
            'error': 'Internal Server Error'
        }), 500

    @app.errorhandler(422)
    def validation_error(error):
        return jsonify({
            'success': False,
            'message': 'Error de validación',
            'error': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'message': 'No autorizado - Token requerido o inválido',
            'error': 'Unauthorized'
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'message': 'Prohibido - Permisos insuficientes',
            'error': 'Forbidden'
        }), 403


if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
