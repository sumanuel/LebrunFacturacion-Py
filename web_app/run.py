#!/usr/bin/env python3
"""
Script de ejecución para la aplicación web Lebrun Facturación
"""
import os
import sys
from application import create_app

def main():
    """Función principal"""
    # Determinar el entorno
    env = os.environ.get('FLASK_ENV') or 'development'

    # Crear aplicación
    app = create_app(env)

    # Configurar host y puerto
    host = os.environ.get('FLASK_HOST') or '127.0.0.1'
    port = int(os.environ.get('FLASK_PORT') or 5000)
    debug = env == 'development'

    print(f"🚀 Iniciando {app.config['APP_NAME']} v{app.config['APP_VERSION']}")
    print(f"🌐 Modo: {env}")
    print(f"📡 Servidor: http://{host}:{port}")
    print("=" * 50)

    # Ejecutar aplicación
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True,
        use_reloader=debug
    )

if __name__ == '__main__':
    # Verificar Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        sys.exit(1)

    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")
        sys.exit(1)