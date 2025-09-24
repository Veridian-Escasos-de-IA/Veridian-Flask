"""
Core del sistema
"""

from .database import db, init_extensions
from .config import config

__all__ = ['db', 'init_extensions', 'config']