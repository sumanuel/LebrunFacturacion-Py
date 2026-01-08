from flask import Blueprint, render_template, session, flash, redirect, url_for
from flask_login import login_required, current_user
import logging

logger = logging.getLogger(__name__)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/index')
@login_required
def index():
    """Página principal del dashboard"""
    try:
        # Obtener menú del usuario desde la sesión (temporalmente vacío)
        menu_data = session.get('menu_data', {})
        empresa_actual = session.get('empresa_actual', {})

        # Generar HTML del menú (placeholder por ahora)
        menu_html = "<!-- Menú no implementado aún -->"

        # Estadísticas del dashboard
        stats = {
            'facturas_hoy': 0,
            'total_ventas': 0.0,
            'clientes_activos': 0,
            'productos_stock': 0
        }

        # Obtener empresa actual como objeto
        from app.models import Compania
        empresa_obj = None
        if empresa_actual:
            empresa_obj = Compania.query.filter_by(codigo=empresa_actual).first()

        return render_template('dashboard/dashboard.html',
                             menu_html=menu_html,
                             empresa_actual=empresa_obj,
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
