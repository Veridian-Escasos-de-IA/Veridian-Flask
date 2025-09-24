"""
API endpoints para autenticación y gestión de usuarios con OAuth
"""

import json
import requests
from flask import Blueprint, request, current_app, url_for, redirect, session
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from datetime import datetime
from authlib.integrations.flask_client import OAuth

from app.core.database import db
from app.models import User
from app.schemas import UserRegistrationSchema, UserLoginSchema
from app.utils import success_response, error_response, validate_json

# Crear Blueprint para autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Configurar OAuth
oauth = OAuth()


@auth_bp.route('/register', methods=['POST'])
@validate_json(UserRegistrationSchema)
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Registrar nuevo usuario',
    'description': 'Registra un nuevo usuario en el sistema',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'ci': {'type': 'string', 'example': '12345678'},
                    'nombres': {'type': 'string', 'example': 'Juan Carlos'},
                    'apellido_paterno': {'type': 'string', 'example': 'Pérez'},
                    'apellido_materno': {'type': 'string', 'example': 'González'},
                    'fecha_nacimiento': {'type': 'string', 'format': 'date', 'example': '1990-05-15'},
                    'sexo': {'type': 'string', 'enum': ['M', 'F'], 'example': 'M'},
                    'telefono': {'type': 'string', 'example': '78901234'},
                    'correo': {'type': 'string', 'format': 'email', 'example': 'juan@email.com'},
                    'direccion': {'type': 'string', 'example': 'Av. Principal 123'},
                    'password': {'type': 'string', 'example': 'password123'},
                    'password_confirm': {'type': 'string', 'example': 'password123'}
                },
                'required': ['ci', 'nombres', 'apellido_paterno', 'fecha_nacimiento', 'sexo', 'correo', 'password', 'password_confirm']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuario registrado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string', 'example': 'Usuario registrado exitosamente'},
                            'user': {'type': 'object'},
                            'access_token': {'type': 'string'},
                            'refresh_token': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Usuario ya existe o datos inválidos'
        },
        422: {
            'description': 'Errores de validación'
        }
    }
})
def register():
    """Registrar un nuevo usuario"""
    try:
        data = request.validated_data
        
        # Verificar si ya existe un usuario con el mismo CI o correo
        existing_user = User.query.filter(
            (User.ci == data['ci']) | (User.correo == data['correo'])
        ).first()
        
        if existing_user:
            if existing_user.ci == data['ci']:
                return error_response('Ya existe un usuario registrado con este CI', 400)
            else:
                return error_response('Ya existe un usuario registrado con este correo electrónico', 400)
        
        # Crear nuevo usuario
        new_user = User(
            ci=data['ci'],
            nombres=data['nombres'],
            apellido_paterno=data['apellido_paterno'],
            apellido_materno=data.get('apellido_materno'),
            fecha_nacimiento=data['fecha_nacimiento'],
            sexo=data['sexo'],
            telefono=data.get('telefono'),
            correo=data['correo'],
            direccion=data.get('direccion'),
            rol='user'  # Rol por defecto
        )
        
        # Establecer contraseña
        new_user.set_password(data['password'])
        
        # Guardar en base de datos
        db.session.add(new_user)
        db.session.commit()
        
        # Crear tokens
        access_token = create_access_token(identity=new_user.ci)
        refresh_token = create_refresh_token(identity=new_user.ci)
        
        return success_response({
            'message': 'Usuario registrado exitosamente',
            'user': new_user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error interno del servidor: {str(e)}', 500)


@auth_bp.route('/login', methods=['POST'])
@validate_json(UserLoginSchema)
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Iniciar sesión',
    'description': 'Autentica un usuario y devuelve tokens JWT',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'correo': {'type': 'string', 'format': 'email', 'example': 'juan@email.com'},
                    'password': {'type': 'string', 'example': 'password123'}
                },
                'required': ['correo', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Inicio de sesión exitoso',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string', 'example': 'Inicio de sesión exitoso'},
                            'user': {'type': 'object'},
                            'access_token': {'type': 'string'},
                            'refresh_token': {'type': 'string'}
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Credenciales inválidas'
        },
        422: {
            'description': 'Errores de validación'
        }
    }
})
def login():
    """Iniciar sesión"""
    try:
        data = request.validated_data
        
        # Buscar usuario por correo
        user = User.query.filter_by(correo=data['correo']).first()
        
        if not user or not user.check_password(data['password']):
            return error_response('Credenciales inválidas', 401)
        
        if not user.activo:
            return error_response('Cuenta de usuario inactiva', 401)
        
        # Actualizar último acceso
        user.ultimo_acceso = datetime.utcnow()
        db.session.commit()
        
        # Crear tokens
        access_token = create_access_token(identity=user.ci)
        refresh_token = create_refresh_token(identity=user.ci)
        
        return success_response({
            'message': 'Inicio de sesión exitoso',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        
    except Exception as e:
        return error_response(f'Error interno del servidor: {str(e)}', 500)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Renovar token de acceso',
    'description': 'Genera un nuevo token de acceso usando el refresh token',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Token renovado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'}
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Token inválido'
        }
    }
})
def refresh():
    """Renovar token de acceso"""
    try:
        current_user_ci = get_jwt_identity()
        
        # Verificar que el usuario aún existe y está activo
        user = User.query.get(current_user_ci)
        if not user or not user.activo:
            return error_response('Usuario no válido o inactivo', 401)
        
        # Crear nuevo token de acceso
        access_token = create_access_token(identity=current_user_ci)
        
        return success_response({
            'access_token': access_token
        })
        
    except Exception as e:
        return error_response(f'Error interno del servidor: {str(e)}', 500)


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Obtener perfil de usuario',
    'description': 'Obtiene la información del usuario autenticado',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Perfil de usuario obtenido exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'user': {'type': 'object'}
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Token inválido o usuario no encontrado'
        }
    }
})
def get_current_user():
    """Obtener información del usuario autenticado"""
    try:
        current_user_ci = get_jwt_identity()
        user = User.query.get(current_user_ci)
        
        if not user or not user.activo:
            return error_response('Usuario no válido o inactivo', 401)
        
        return success_response({
            'user': user.to_dict()
        })
        
    except Exception as e:
        return error_response(f'Error interno del servidor: {str(e)}', 500)


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Cerrar sesión',
    'description': 'Cierra la sesión del usuario (informativo, los tokens JWT deben manejarse en el cliente)',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Sesión cerrada exitosamente'
        }
    }
})
def logout():
    """Cerrar sesión"""
    # Nota: JWT son stateless, por lo que el logout es principalmente informativo
    # En una implementación más avanzada se podría usar una blacklist de tokens
    
    return success_response({
        'message': 'Sesión cerrada exitosamente. El token debe ser eliminado del cliente.'
    })


# ========== OAUTH GOOGLE ==========

def init_oauth(app):
    """Inicializar OAuth con la aplicación Flask"""
    oauth.init_app(app)
    
    google = oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    return google


@auth_bp.route('/google/login', methods=['GET'])
@swag_from({
    'tags': ['OAuth'],
    'summary': 'Iniciar login con Google',
    'description': 'Redirige al usuario a Google para autenticación OAuth',
    'responses': {
        302: {
            'description': 'Redirección a Google OAuth'
        }
    }
})
def google_login():
    """Iniciar el proceso de login con Google"""
    try:
        google = oauth.google
        redirect_uri = url_for('auth.google_callback', _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        return error_response(f'Error al iniciar OAuth: {str(e)}', 500)


@auth_bp.route('/google/callback', methods=['GET'])
@swag_from({
    'tags': ['OAuth'],
    'summary': 'Callback de Google OAuth',
    'description': 'Procesa la respuesta de Google OAuth y autentica al usuario',
    'responses': {
        200: {
            'description': 'Usuario autenticado exitosamente'
        },
        400: {
            'description': 'Error en la autenticación OAuth'
        }
    }
})
def google_callback():
    """Callback después del login con Google"""
    try:
        google = oauth.google
        token = google.authorize_access_token()
        
        # Obtener información del usuario de Google
        user_info = token.get('userinfo')
        if not user_info:
            return error_response('No se pudo obtener información del usuario', 400)
        
        email = user_info.get('email')
        if not email:
            return error_response('Email no proporcionado por Google', 400)
        
        # Buscar usuario existente
        user = User.query.filter_by(correo=email).first()
        
        if user:
            # Usuario existente - actualizar información OAuth
            user.provider = 'google'
            user.provider_id = user_info.get('sub')
            user.avatar_url = user_info.get('picture')
            user.ultimo_acceso = datetime.utcnow()
            
        else:
            # Crear nuevo usuario OAuth
            nombres = user_info.get('given_name', '')
            apellido = user_info.get('family_name', '')
            
            user = User(
                ci=f"GOOGLE_{user_info.get('sub')}",  # CI temporal para OAuth users
                nombres=nombres,
                apellido_paterno=apellido or 'OAuth',
                apellido_materno=None,
                fecha_nacimiento=datetime(1990, 1, 1).date(),  # Fecha por defecto
                sexo='N',  # No especificado
                correo=email,
                provider='google',
                provider_id=user_info.get('sub'),
                avatar_url=user_info.get('picture'),
                activo=True,
                rol='user'
            )
            
            db.session.add(user)
        
        db.session.commit()
        
        # Crear tokens JWT
        access_token = create_access_token(identity=user.ci)
        refresh_token = create_refresh_token(identity=user.ci)
        
        # Para frontend web, podemos devolver los tokens en query params
        # o usar algún mecanismo de comunicación
        frontend_url = current_app.config.get('CORS_ORIGINS', ['http://localhost:5173'])[0]
        
        return redirect(f"{frontend_url}/auth/callback?access_token={access_token}&refresh_token={refresh_token}&user={user.ci}")
        
    except Exception as e:
        return error_response(f'Error en callback OAuth: {str(e)}', 500)


@auth_bp.route('/google/user', methods=['POST'])
@swag_from({
    'tags': ['OAuth'],
    'summary': 'Autenticar con datos de Google',
    'description': 'Autentica directamente con datos del token de Google (para frontend)',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_token': {'type': 'string', 'description': 'Token ID de Google'},
                    'access_token': {'type': 'string', 'description': 'Access token de Google'}
                },
                'required': ['id_token']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario autenticado exitosamente'
        }
    }
})
def google_user_auth():
    """Autenticar usuario con token de Google (para frontend)"""
    try:
        data = request.get_json()
        id_token = data.get('id_token')
        
        if not id_token:
            return error_response('Token ID requerido', 400)
        
        # Verificar token con Google
        google_verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
        response = requests.get(google_verify_url)
        
        if response.status_code != 200:
            return error_response('Token inválido', 400)
        
        user_info = response.json()
        email = user_info.get('email')
        
        if not email:
            return error_response('Email no encontrado en token', 400)
        
        # Buscar o crear usuario
        user = User.query.filter_by(correo=email).first()
        
        if user:
            # Actualizar información OAuth
            user.provider = 'google'
            user.provider_id = user_info.get('sub')
            user.avatar_url = user_info.get('picture')
            user.ultimo_acceso = datetime.utcnow()
            
        else:
            # Crear nuevo usuario
            user = User(
                ci=f"GOOGLE_{user_info.get('sub')}",
                nombres=user_info.get('given_name', ''),
                apellido_paterno=user_info.get('family_name', 'OAuth'),
                apellido_materno=None,
                fecha_nacimiento=datetime(1990, 1, 1).date(),
                sexo='N',
                correo=email,
                provider='google',
                provider_id=user_info.get('sub'),
                avatar_url=user_info.get('picture'),
                activo=True,
                rol='user'
            )
            
            db.session.add(user)
        
        db.session.commit()
        
        # Crear tokens JWT
        access_token = create_access_token(identity=user.ci)
        refresh_token = create_refresh_token(identity=user.ci)
        
        return success_response({
            'message': 'Usuario autenticado exitosamente con Google',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        
    except Exception as e:
        return error_response(f'Error en autenticación Google: {str(e)}', 500)


@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Autenticación'],
    'summary': 'Verificar token de acceso',
    'description': 'Verifica la validez del token JWT y retorna la información del usuario',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Token válido',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'user': {'type': 'object'},
                            'is_valid': {'type': 'boolean', 'example': True}
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Token inválido o expirado'
        }
    }
})
def verify_token():
    """Verificar token de acceso y obtener información del usuario"""
    try:
        # Obtener CI del usuario desde el token
        user_ci = get_jwt_identity()
        
        # Buscar usuario en la base de datos
        user = User.query.filter_by(ci=user_ci).first()
        
        if not user:
            return error_response('Usuario no encontrado', 404)
        
        return success_response({
            'user': user.to_dict(),
            'is_valid': True
        })
        
    except Exception as e:
        return error_response(f'Error verificando token: {str(e)}', 500)