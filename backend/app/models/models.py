"""
Modelos SQLAlchemy para el Sistema de Gestión del Edificio Multifuncional
Basados en el esquema real de PostgreSQL de la base de datos "Edificio"
"""

from app.core.database import db
from datetime import datetime
import bcrypt


class PersonaBase(db.Model):
    """
    Modelo principal de Persona basado en el esquema real de PostgreSQL
    Esta tabla es la base para todas las relaciones del sistema
    """
    __tablename__ = 'persona'
    
    # Campos según esquema real de PostgreSQL
    ci = db.Column(db.String(20), primary_key=True)  # Carnet de identidad
    nombres = db.Column(db.String(120), nullable=False)
    apellido_paterno = db.Column(db.String(120), nullable=True)
    apellido_materno = db.Column(db.String(120), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    sexo = db.Column(db.String(1), nullable=True)  # 'M' o 'F'
    telefono = db.Column(db.String(50), nullable=True)
    correo = db.Column(db.String(150), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    foto_url = db.Column(db.String(300), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    
    # Timestamps
    fecha_creacion = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, ci, nombres, apellido_paterno=None, apellido_materno=None, 
                 fecha_nacimiento=None, sexo=None, telefono=None, correo=None, 
                 direccion=None, foto_url=None, activo=True):
        self.ci = ci
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.foto_url = foto_url
        self.activo = activo
    
    @property
    def nombre_completo(self):
        """Genera el nombre completo de la persona"""
        nombres = [self.nombres]
        if self.apellido_paterno:
            nombres.append(self.apellido_paterno)
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return ' '.join(nombres)
    
    def to_dict(self):
        """Convierte el modelo a diccionario para JSON"""
        return {
            'ci': self.ci,
            'nombres': self.nombres,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            'nombre_completo': self.nombre_completo,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'sexo': self.sexo,
            'telefono': self.telefono,
            'correo': self.correo,
            'direccion': self.direccion,
            'foto_url': self.foto_url,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
    
    def __repr__(self):
        return f'<PersonaBase {self.ci}: {self.nombre_completo}>'


class User(db.Model):
    """
    Modelo de Usuario para autenticación
    Utiliza la tabla 'personas' que ya existe en la DB para compatibilidad con auth
    """
    __tablename__ = 'personas'
    
    ci = db.Column(db.String(20), primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    telefono = db.Column(db.String(15), nullable=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    direccion = db.Column(db.Text, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable para OAuth users
    activo = db.Column(db.Boolean, default=True)
    rol = db.Column(db.String(20), default='user')
    ultimo_acceso = db.Column(db.DateTime, nullable=True)
    
    # OAuth fields
    provider = db.Column(db.String(50), nullable=True)  # 'google', 'local', etc.
    provider_id = db.Column(db.String(255), nullable=True)  # Google ID, etc.
    avatar_url = db.Column(db.String(500), nullable=True)  # Profile picture URL
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Establece la contraseña hasheada"""
        if password:
            self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verifica la contraseña"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def is_oauth_user(self):
        """Verifica si el usuario se autenticó via OAuth"""
        return self.provider and self.provider != 'local'
    
    @property
    def nombre_completo(self):
        """Genera el nombre completo del usuario"""
        nombres = [self.nombres, self.apellido_paterno]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return ' '.join(nombres)
    
    def to_dict(self, include_sensitive=False):
        """Convierte el modelo a diccionario"""
        data = {
            'ci': self.ci,
            'nombres': self.nombres,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            'nombre_completo': self.nombre_completo,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'sexo': self.sexo,
            'telefono': self.telefono,
            'correo': self.correo,
            'direccion': self.direccion,
            'activo': self.activo,
            'rol': self.rol,
            'provider': self.provider,
            'avatar_url': self.avatar_url,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
            
        return data
    
    def __repr__(self):
        return f'<User {self.ci}: {self.correo}>'


# Modelos adicionales del edificio (preparados para futuras funcionalidades)

class Departamento(db.Model):
    """Modelo para departamentos del edificio"""
    __tablename__ = 'departamento'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), nullable=False, unique=True)
    piso = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=True)  # duplex, simple, etc.
    metros_cuadrados = db.Column(db.Numeric(8, 2), nullable=True)
    estado = db.Column(db.String(20), default='disponible')  # disponible, ocupado, mantenimiento
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'piso': self.piso,
            'tipo': self.tipo,
            'metros_cuadrados': float(self.metros_cuadrados) if self.metros_cuadrados else None,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
    
    def __repr__(self):
        return f'<Departamento {self.numero} - Piso {self.piso}>'


class Residente(db.Model):
    """Modelo para residentes del edificio"""
    __tablename__ = 'residentes'
    
    id = db.Column(db.Integer, primary_key=True)
    persona_ci = db.Column(db.String(20), db.ForeignKey('persona.ci'), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=True)
    es_propietario = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    persona = db.relationship('PersonaBase', backref='residencias')
    departamento = db.relationship('Departamento', backref='residentes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'persona_ci': self.persona_ci,
            'departamento_id': self.departamento_id,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'es_propietario': self.es_propietario,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    def __repr__(self):
        return f'<Residente {self.persona_ci} - Depto {self.departamento_id}>'