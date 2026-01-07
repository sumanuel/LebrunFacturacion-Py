from flask import Blueprint, render_template, session, flash, redirect, url_for
from flask_login import login_required, current_user
from app.menu import generar_menu_html
import logging

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/index')
@login_required
def index():
    """Página principal del dashboard"""
    try:
        # Obtener menú del usuario desde la sesión
        menu_data = session.get('menu_data', {})
        empresa_actual = session.get('empresa_actual')

        if not menu_data:
            flash('No se pudo cargar el menú del usuario. Contacte al administrador.', 'warning')
            logger.warning(f'Menú no disponible para usuario {current_user.login}')

        # Generar HTML del menú
        menu_html = generar_menu_html(menu_data)

        # Estadísticas del dashboard
        stats = {
            'facturas_hoy': 0,
            'total_ventas': 0.0,
            'clientes_activos': 0,
            'productos_stock': 0
        }

        # Aquí se cargarían las estadísticas reales desde la base de datos
        # Por ahora, valores de ejemplo

        return render_template('dashboard.html',
                             menu_html=menu_html,
                             empresa_actual=empresa_actual,
                             stats=stats,
                             user=current_user)

    except Exception as e:
        logger.error(f'Error en dashboard: {str(e)}')
        flash('Error cargando el dashboard.', 'danger')
        return redirect(url_for('auth.login'))

@dashboard_bp.route('/stats')
@login_required
def get_stats():
    """API para obtener estadísticas del dashboard"""
    try:
        # Aquí se implementarían consultas reales a la base de datos
        stats = {
            'facturas_hoy': 5,
            'total_ventas': 125000.50,
            'clientes_activos': 150,
            'productos_stock': 2500,
            'timestamp': '2024-01-07T12:00:00Z'
        }

        return {
            'success': True,
            'data': stats
        }

    except Exception as e:
        logger.error(f'Error obteniendo estadísticas: {str(e)}')
        return {
            'success': False,
            'error': 'Error interno del servidor'
        }, 500

@dashboard_bp.route('/menu')
@login_required
def get_menu():
    """API para obtener el menú del usuario"""
    try:
        menu_data = session.get('menu_data', {})
        return {
            'success': True,
            'menu': menu_data
        }

    except Exception as e:
        logger.error(f'Error obteniendo menú: {str(e)}')
        return {
            'success': False,
            'error': 'Error interno del servidor'
        }, 500