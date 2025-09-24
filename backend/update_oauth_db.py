#!/usr/bin/env python3
"""
Script para actualizar la base de datos con campos OAuth
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
load_dotenv()

import psycopg2
from psycopg2.extras import RealDictCursor

def update_database():
    """Actualizar base de datos con campos OAuth"""
    
    # Configuración de conexión
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'Edificio'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'admin')
    }
    
    try:
        print("Conectando a PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("Verificando estructura de tabla personas...")
        
        # Verificar si las columnas OAuth ya existen
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'personas' 
            AND column_name IN ('provider', 'provider_id', 'avatar_url')
        """)
        
        existing_columns = [row['column_name'] for row in cursor.fetchall()]
        
        # Agregar columnas OAuth si no existen
        oauth_columns = [
            ('provider', 'VARCHAR(50)'),
            ('provider_id', 'VARCHAR(255)'),
            ('avatar_url', 'VARCHAR(500)')
        ]
        
        for col_name, col_type in oauth_columns:
            if col_name not in existing_columns:
                print(f"Agregando columna {col_name}...")
                cursor.execute(f"""
                    ALTER TABLE personas 
                    ADD COLUMN {col_name} {col_type}
                """)
        
        # Hacer nullable el password_hash para usuarios OAuth
        print("Actualizando password_hash para OAuth...")
        cursor.execute("""
            ALTER TABLE personas 
            ALTER COLUMN password_hash DROP NOT NULL
        """)
        
        # Confirmar cambios
        conn.commit()
        print("Base de datos actualizada exitosamente!")
        
        # Mostrar estructura actualizada
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'personas'
            ORDER BY ordinal_position
        """)
        
        print("\nEstructura actual de tabla 'personas':")
        for row in cursor.fetchall():
            nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
            print(f"  - {row['column_name']}: {row['data_type']} ({nullable})")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    update_database()