"""
Esquemas de validación para la API usando Marshmallow
"""

from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from datetime import datetime, date
import re


class PersonaCreateSchema(Schema):
    """Esquema para validar la creación de personas"""
    ci = fields.Str(required=True, validate=lambda x: len(x.strip()) >= 3)
    nombres = fields.Str(required=True, validate=lambda x: len(x.strip()) >= 2)
    apellido_paterno = fields.Str(required=False, allow_none=True)
    apellido_materno = fields.Str(required=False, allow_none=True)
    fecha_nacimiento = fields.Date(required=False, allow_none=True)
    sexo = fields.Str(required=False, allow_none=True, validate=lambda x: x in ['M', 'F'])
    telefono = fields.Str(required=False, allow_none=True)
    correo = fields.Email(required=False, allow_none=True)
    direccion = fields.Str(required=False, allow_none=True)
    foto_url = fields.Url(required=False, allow_none=True)
    activo = fields.Bool(missing=True)

    @validates('ci')
    def validate_ci(self, value):
        """Validar formato del CI"""
        if not value or not value.strip():
            raise ValidationError('CI es requerido')
        
        ci_clean = value.strip()
        if len(ci_clean) < 3:
            raise ValidationError('CI debe tener al menos 3 caracteres')
        
        # Validar que sea alfanumérico
        if not ci_clean.isalnum():
            raise ValidationError('CI debe contener solo letras y números')

    @validates('telefono')
    def validate_telefono(self, value):
        """Validar formato del teléfono"""
        if value and value.strip():
            phone_clean = re.sub(r'[^\d]', '', value)
            if len(phone_clean) < 7 or len(phone_clean) > 15:
                raise ValidationError('Teléfono debe tener entre 7 y 15 dígitos')

    @validates('fecha_nacimiento')
    def validate_fecha_nacimiento(self, value):
        """Validar fecha de nacimiento"""
        if value:
            today = date.today()
            if value > today:
                raise ValidationError('Fecha de nacimiento no puede ser futura')
            
            # Validar edad mínima y máxima razonable
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 0 or age > 120:
                raise ValidationError('Edad debe estar entre 0 y 120 años')


class PersonaUpdateSchema(Schema):
    """Esquema para validar la actualización de personas"""
    nombres = fields.Str(required=False)
    apellido_paterno = fields.Str(required=False, allow_none=True)
    apellido_materno = fields.Str(required=False, allow_none=True)
    fecha_nacimiento = fields.Date(required=False, allow_none=True)
    sexo = fields.Str(required=False, allow_none=True, validate=lambda x: x in ['M', 'F'])
    telefono = fields.Str(required=False, allow_none=True)
    correo = fields.Email(required=False, allow_none=True)
    direccion = fields.Str(required=False, allow_none=True)
    foto_url = fields.Url(required=False, allow_none=True)
    activo = fields.Bool(required=False)

    @validates('telefono')
    def validate_telefono(self, value):
        """Validar formato del teléfono"""
        if value and value.strip():
            phone_clean = re.sub(r'[^\d]', '', value)
            if len(phone_clean) < 7 or len(phone_clean) > 15:
                raise ValidationError('Teléfono debe tener entre 7 y 15 dígitos')

    @validates('fecha_nacimiento')
    def validate_fecha_nacimiento(self, value):
        """Validar fecha de nacimiento"""
        if value:
            today = date.today()
            if value > today:
                raise ValidationError('Fecha de nacimiento no puede ser futura')
            
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 0 or age > 120:
                raise ValidationError('Edad debe estar entre 0 y 120 años')


class UserRegistrationSchema(Schema):
    """Esquema para validar el registro de usuarios"""
    ci = fields.Str(required=True)
    nombres = fields.Str(required=True)
    apellido_paterno = fields.Str(required=True)
    apellido_materno = fields.Str(required=False, allow_none=True)
    fecha_nacimiento = fields.Date(required=True)
    sexo = fields.Str(required=True, validate=lambda x: x in ['M', 'F'])
    telefono = fields.Str(required=False, allow_none=True)
    correo = fields.Email(required=True)
    direccion = fields.Str(required=False, allow_none=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    password_confirm = fields.Str(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        """Validar que las contraseñas coincidan"""
        if data.get('password') != data.get('password_confirm'):
            raise ValidationError('Las contraseñas no coinciden', 'password_confirm')

    @validates('ci')
    def validate_ci(self, value):
        """Validar formato del CI"""
        if not value or not value.strip():
            raise ValidationError('CI es requerido')
        
        ci_clean = value.strip()
        if len(ci_clean) < 3:
            raise ValidationError('CI debe tener al menos 3 caracteres')
        
        if not ci_clean.isalnum():
            raise ValidationError('CI debe contener solo letras y números')

    @validates('password')
    def validate_password(self, value):
        """Validar fortaleza de la contraseña"""
        if len(value) < 6:
            raise ValidationError('Contraseña debe tener al menos 6 caracteres')
        
        # Verificar que contenga al menos una letra y un número
        has_letter = any(c.isalpha() for c in value)
        has_number = any(c.isdigit() for c in value)
        
        if not (has_letter and has_number):
            raise ValidationError('Contraseña debe contener al menos una letra y un número')


class UserLoginSchema(Schema):
    """Esquema para validar el login de usuarios"""
    correo = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates('correo')
    def validate_correo(self, value):
        """Validar que el correo no esté vacío"""
        if not value or not value.strip():
            raise ValidationError('Correo electrónico es requerido')

    @validates('password')
    def validate_password(self, value):
        """Validar que la contraseña no esté vacía"""
        if not value or not value.strip():
            raise ValidationError('Contraseña es requerida')


class DepartamentoSchema(Schema):
    """Esquema para validar departamentos"""
    numero = fields.Str(required=True)
    piso = fields.Int(required=True, validate=lambda x: x > 0)
    tipo = fields.Str(required=False, allow_none=True)
    metros_cuadrados = fields.Decimal(required=False, allow_none=True, places=2)
    estado = fields.Str(required=False, missing='disponible', 
                       validate=lambda x: x in ['disponible', 'ocupado', 'mantenimiento'])

    @validates('numero')
    def validate_numero(self, value):
        """Validar número de departamento"""
        if not value or not value.strip():
            raise ValidationError('Número de departamento es requerido')

    @validates('piso')
    def validate_piso(self, value):
        """Validar piso"""
        if value < 1 or value > 50:  # Rango razonable
            raise ValidationError('Piso debe estar entre 1 y 50')


class ResidenteSchema(Schema):
    """Esquema para validar residentes"""
    persona_ci = fields.Str(required=True)
    departamento_id = fields.Int(required=True)
    fecha_inicio = fields.Date(required=True)
    fecha_fin = fields.Date(required=False, allow_none=True)
    es_propietario = fields.Bool(missing=False)
    activo = fields.Bool(missing=True)

    @validates_schema
    def validate_fechas(self, data, **kwargs):
        """Validar que las fechas sean lógicas"""
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise ValidationError('Fecha fin debe ser posterior a fecha inicio', 'fecha_fin')

    @validates('fecha_inicio')
    def validate_fecha_inicio(self, value):
        """Validar fecha de inicio"""
        if value and value > date.today():
            raise ValidationError('Fecha de inicio no puede ser futura')