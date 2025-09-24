"""
Esquemas de validación
"""

from .schemas import (
    PersonaCreateSchema,
    PersonaUpdateSchema,
    UserRegistrationSchema,
    UserLoginSchema,
    DepartamentoSchema,
    ResidenteSchema
)

__all__ = [
    'PersonaCreateSchema',
    'PersonaUpdateSchema', 
    'UserRegistrationSchema',
    'UserLoginSchema',
    'DepartamentoSchema',
    'ResidenteSchema'
]