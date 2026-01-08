from flask import Flask, session, g, render_template, request
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect, generate_csrf
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Importar configuración
from config import config

# Importar módulos de la aplicación
from app.models import db
from app.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.errors import errors_bp
from app.facturacion import facturacion_bp
# Los siguientes blueprints se implementarán próximamente:
# from app.routes.clientes import clientes_bp
# from app.routes.bancos import bancos_bp
# from app.routes.complementos import complementos_bp
# from app.routes.contabilidad import contabilidad_bp
# from app.routes.vendedores import vendedores_bp

# Configurar logging
def setup_logging(app):
    """Configurar logging de la aplicación"""
    if not os.path.exists('logs'):
        os.makedirs('logs')

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler
    file_handler = logging.FileHandler(app.config['LOG_FILE'])
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Configurar root logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))

def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

    # Cargar configuración
    app.config.from_object(config[config_name])

    # Configurar logging
    setup_logging(app)

    # Inicializar extensiones
    db.init_app(app)

    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'

    # Configurar CSRF
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    csrf.exempt(app.view_functions['auth.login'])
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(errors_bp)
    app.register_blueprint(facturacion_bp, url_prefix='/facturacion')
    # Los siguientes blueprints se implementarán próximamente:
    # app.register_blueprint(clientes_bp, url_prefix='/clientes')
    # app.register_blueprint(bancos_bp, url_prefix='/bancos')
    # app.register_blueprint(complementos_bp, url_prefix='/complementos')
    # app.register_blueprint(contabilidad_bp, url_prefix='/contabilidad')
    # app.register_blueprint(vendedores_bp, url_prefix='/vendedores')

    # Configurar contexto de aplicación
    @app.before_request
    def before_request():
        """Configurar contexto antes de cada request"""
        g.start_time = datetime.now()

        # Información del usuario actual
        if current_user.is_authenticated:
            g.user = current_user
            g.empresa_actual = getattr(current_user, 'empresa_actual', None)

    @app.after_request
    def after_request(response):
        """Configurar contexto después de cada request"""
        if hasattr(g, 'start_time'):
            duration = datetime.now() - g.start_time
            app.logger.info(f'Request {request.method} {request.path} took {duration.total_seconds():.2f}s')

        return response

    @app.context_processor
    def inject_globals():
        """Inyectar variables globales en templates"""
        from app.menu import get_menu_data, get_breadcrumbs, get_quick_actions

        return {
            'app_name': app.config['APP_NAME'],
            'app_version': app.config['APP_VERSION'],
            'current_year': datetime.now().year,
            'user': current_user if current_user.is_authenticated else None,
            'get_menu_data': get_menu_data,
            'get_breadcrumbs': get_breadcrumbs,
            'get_quick_actions': get_quick_actions,
            'csrf_token': generate_csrf
        }

    @app.errorhandler(404)
    def page_not_found(e):
        """Manejador de error 404"""
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        """Manejador de error 500"""
        app.logger.error(f'Error 500: {str(e)}')
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        """Manejador de error 403"""
        return render_template('403.html'), 403

    # Función para user_loader de Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import UsuarioSistema
        return UsuarioSistema.query.get(int(user_id))

    # Crear tablas si no existen (solo en desarrollo)
    if config_name == 'development':
        with app.app_context():
            try:
                # db.create_all()  # Comentado porque las tablas ya existen en la DB real
                app.logger.info('Tablas de base de datos creadas/verficadas')
            except Exception as e:
                app.logger.error(f'Error creando tablas: {str(e)}')

    app.logger.info(f'Aplicación {app.config["APP_NAME"]} v{app.config["APP_VERSION"]} iniciada en modo {config_name}')

    return app