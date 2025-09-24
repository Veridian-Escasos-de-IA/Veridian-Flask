#!/usr/bin/env python3
"""
Punto de entrada para el Sistema de Gestión del Edificio Multifuncional
"""

import os
import sys
from dotenv import load_dotenv

# Agregar el directorio actual (backend) al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Cargar variables de entorno
load_dotenv()

# Importar create_app desde el módulo app/app.py
try:
    from app.app import create_app
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Directorio actual:", current_dir)
    print("Contenido del directorio:")
    for item in os.listdir(current_dir):
        print(f"  - {item}")
    sys.exit(1)

# Crear la aplicación
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print("="*60)
    print("Sistema de Gestión del Edificio Multifuncional")
    print("="*60)
    print(f"Servidor: http://127.0.0.1:{port}")
    print(f"Documentación: http://127.0.0.1:{port}/docs/")
    print(f"Estado: http://127.0.0.1:{port}/health")
    print("="*60)

    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port,
        threaded=True
    )
