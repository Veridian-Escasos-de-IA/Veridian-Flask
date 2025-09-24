"""
API endpoints para gestión de personas
"""

from flask import Blueprint, request
from flasgger import swag_from
from datetime import datetime

from app.core.database import db
from app.models import PersonaBase
from app.schemas import PersonaCreateSchema, PersonaUpdateSchema
from app.utils import success_response, error_response, validate_json, validation_error_response

# Crear Blueprint para personas
personas_bp = Blueprint('personas', __name__, url_prefix='/api/personas')


def parse_date(date_string):
    """Convierte string de fecha a objeto date"""
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError(f"Formato de fecha inválido: {date_string}. Use YYYY-MM-DD")


@personas_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Personas'],
    'summary': 'Listar todas las personas',
    'description': 'Obtiene una lista paginada de todas las personas registradas en el sistema',
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'default': 1,
            'description': 'Número de página'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'description': 'Elementos por página (máximo 100)'
        },
        {
            'name': 'activo',
            'in': 'query',
            'type': 'boolean',
            'description': 'Filtrar por estado activo'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de personas obtenida exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'personas': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'ci': {'type': 'string'},
                                        'nombres': {'type': 'string'},
                                        'apellido_paterno': {'type': 'string'},
                                        'apellido_materno': {'type': 'string'},
                                        'nombre_completo': {'type': 'string'},
                                        'correo': {'type': 'string'},
                                        'telefono': {'type': 'string'},
                                        'activo': {'type': 'boolean'}
                                    }
                                }
                            },
                            'total': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def listar_personas():
    """Obtener lista paginada de todas las personas"""
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # Filtros
        activo = request.args.get('activo', type=bool)
        
        # Query base
        query = PersonaBase.query
        
        # Aplicar filtros
        if activo is not None:
            query = query.filter_by(activo=activo)
        
        # Paginación
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        personas_data = [persona.to_dict() for persona in pagination.items]
        
        return success_response({
            'personas': personas_data,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        })
        
    except Exception as e:
        return error_response(f'Error al obtener personas: {str(e)}', 500)


@personas_bp.route('/', methods=['POST'])
@validate_json(PersonaCreateSchema)
@swag_from({
    'tags': ['Personas'],
    'summary': 'Crear nueva persona',
    'description': 'Registra una nueva persona en el sistema',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'ci': {'type': 'string', 'example': '12345678', 'description': 'Carnet de identidad'},
                    'nombres': {'type': 'string', 'example': 'Juan Carlos', 'description': 'Nombres de la persona'},
                    'apellido_paterno': {'type': 'string', 'example': 'Pérez', 'description': 'Apellido paterno'},
                    'apellido_materno': {'type': 'string', 'example': 'González', 'description': 'Apellido materno (opcional)'},
                    'fecha_nacimiento': {'type': 'string', 'format': 'date', 'example': '1990-05-15'},
                    'sexo': {'type': 'string', 'enum': ['M', 'F'], 'example': 'M'},
                    'telefono': {'type': 'string', 'example': '78901234', 'description': 'Teléfono (opcional)'},
                    'correo': {'type': 'string', 'format': 'email', 'example': 'juan@email.com'},
                    'direccion': {'type': 'string', 'example': 'Av. Principal 123', 'description': 'Dirección (opcional)'},
                    'foto_url': {'type': 'string', 'example': 'https://example.com/foto.jpg', 'description': 'URL de foto (opcional)'}
                },
                'required': ['ci', 'nombres']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Persona creada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'message': {'type': 'string', 'example': 'Persona creada exitosamente'},
                            'persona': {'type': 'object'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Datos inválidos o persona ya existe'
        },
        422: {
            'description': 'Errores de validación'
        }
    }
})
def crear_persona():
    """Crear una nueva persona"""
    try:
        data = request.validated_data
        
        # Verificar si ya existe una persona con el mismo CI
        existing_persona = PersonaBase.query.filter_by(ci=data['ci']).first()
        if existing_persona:
            return error_response('Ya existe una persona registrada con este CI', 400)
        
        # Obtener fecha - Marshmallow ya la convierte
        fecha_nacimiento = data.get('fecha_nacimiento')
        
        # Crear nueva persona
        nueva_persona = PersonaBase(
            ci=data['ci'],
            nombres=data['nombres'],
            apellido_paterno=data.get('apellido_paterno'),
            apellido_materno=data.get('apellido_materno'),
            fecha_nacimiento=fecha_nacimiento,
            sexo=data.get('sexo'),
            telefono=data.get('telefono'),
            correo=data.get('correo'),
            direccion=data.get('direccion'),
            foto_url=data.get('foto_url'),
            activo=data.get('activo', True)
        )
        
        # Guardar en base de datos
        db.session.add(nueva_persona)
        db.session.commit()
        
        return success_response({
            'message': 'Persona creada exitosamente',
            'persona': nueva_persona.to_dict()
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error interno del servidor: {str(e)}', 500)


@personas_bp.route('/<ci>', methods=['GET'])
@swag_from({
    'tags': ['Personas'],
    'summary': 'Obtener persona por CI',
    'description': 'Obtiene los datos de una persona específica por su CI',
    'parameters': [
        {
            'name': 'ci',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'CI de la persona'
        }
    ],
    'responses': {
        200: {
            'description': 'Persona encontrada'
        },
        404: {
            'description': 'Persona no encontrada'
        }
    }
})
def obtener_persona(ci):
    """Obtener una persona por CI"""
    try:
        persona = PersonaBase.query.filter_by(ci=ci).first()
        
        if not persona:
            return error_response('Persona no encontrada', 404)
        
        return success_response({
            'persona': persona.to_dict()
        })
        
    except Exception as e:
        return error_response(f'Error al obtener persona: {str(e)}', 500)


@personas_bp.route('/<ci>', methods=['PUT'])
@validate_json(PersonaUpdateSchema)
@swag_from({
    'tags': ['Personas'],
    'summary': 'Actualizar persona',
    'description': 'Actualiza los datos de una persona existente',
    'parameters': [
        {
            'name': 'ci',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'CI de la persona'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombres': {'type': 'string'},
                    'apellido_paterno': {'type': 'string'},
                    'apellido_materno': {'type': 'string'},
                    'fecha_nacimiento': {'type': 'string', 'format': 'date'},
                    'sexo': {'type': 'string', 'enum': ['M', 'F']},
                    'telefono': {'type': 'string'},
                    'correo': {'type': 'string', 'format': 'email'},
                    'direccion': {'type': 'string'},
                    'foto_url': {'type': 'string'},
                    'activo': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Persona actualizada exitosamente'
        },
        404: {
            'description': 'Persona no encontrada'
        },
        422: {
            'description': 'Errores de validación'
        }
    }
})
def actualizar_persona(ci):
    """Actualizar una persona existente"""
    try:
        persona = PersonaBase.query.filter_by(ci=ci).first()
        
        if not persona:
            return error_response('Persona no encontrada', 404)
        
        data = request.validated_data
        
        # Actualizar campos
        for field, value in data.items():
            if hasattr(persona, field):
                setattr(persona, field, value)
        
        # Actualizar timestamp
        persona.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return success_response({
            'message': 'Persona actualizada exitosamente',
            'persona': persona.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al actualizar persona: {str(e)}', 500)


@personas_bp.route('/<ci>', methods=['DELETE'])
@swag_from({
    'tags': ['Personas'],
    'summary': 'Eliminar persona',
    'description': 'Marca una persona como inactiva (eliminación suave)',
    'parameters': [
        {
            'name': 'ci',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'CI de la persona'
        }
    ],
    'responses': {
        200: {
            'description': 'Persona eliminada exitosamente'
        },
        404: {
            'description': 'Persona no encontrada'
        }
    }
})
def eliminar_persona(ci):
    """Eliminar una persona (eliminación suave)"""
    try:
        persona = PersonaBase.query.filter_by(ci=ci).first()
        
        if not persona:
            return error_response('Persona no encontrada', 404)
        
        # Eliminación suave - marcar como inactiva
        persona.activo = False
        persona.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return success_response({
            'message': 'Persona eliminada exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error al eliminar persona: {str(e)}', 500)