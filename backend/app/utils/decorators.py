"""
Decoradores para la API
"""

from functools import wraps
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.utils.responses import validation_error_response
from app.models import User


def validate_json(schema_class):
    """
    Decorador para validar JSON usando esquemas de Marshmallow
    
    Args:
        schema_class: Clase del esquema de Marshmallow
    
    Returns:
        Decorador que valida el JSON de entrada
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return validation_error_response({'_schema': ['Content-Type debe ser application/json']})
            
            try:
                schema = schema_class()
                data = schema.load(request.get_json())
                request.validated_data = data
                return f(*args, **kwargs)
            except ValidationError as e:
                return validation_error_response(e.messages)
                
        return decorated_function
    return decorator


def require_role(role):
    """
    Decorador que requiere un rol específico
    
    Args:
        role: Rol requerido ('admin', 'user', etc.)
    
    Returns:
        Decorador que verifica el rol del usuario
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_ci = get_jwt_identity()
            user = User.query.get(current_user_ci)
            
            if not user or not user.activo:
                return validation_error_response({'auth': ['Usuario no válido o inactivo']})
            
            if user.rol != role and user.rol != 'admin':  # Admin siempre tiene acceso
                return validation_error_response({'auth': [f'Se requiere rol {role}']})
            
            request.current_user = user
            return f(*args, **kwargs)
            
        return decorated_function
    return decorator


def require_auth():
    """
    Decorador que requiere autenticación
    
    Returns:
        Decorador que verifica que el usuario esté autenticado
    """
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_ci = get_jwt_identity()
            user = User.query.get(current_user_ci)
            
            if not user or not user.activo:
                return validation_error_response({'auth': ['Usuario no válido o inactivo']})
            
            request.current_user = user
            return f(*args, **kwargs)
            
        return decorated_function
    return decorator