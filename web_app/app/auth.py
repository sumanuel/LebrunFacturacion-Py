"""
Sistema de autenticación para Lebrun Facturación Web
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import logging

from app.models import UsuarioSistema, Compania, SesionUsuario, db

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    # Redirigir si ya está autenticado
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    # Obtener compañías activas para mostrar en el formulario
    companies = Compania.query.filter_by(activo=1).all()

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        company_code = request.form.get('company', '').strip()

        # Validar campos obligatorios
        if not username or not password or not company_code:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('login.html', companies=companies)

        try:
            # Buscar usuario
            user = UsuarioSistema.query.filter_by(login=username).first()

            if not user:
                flash('Usuario no encontrado.', 'error')
                logger.warning(f'Intento de login fallido: usuario {username} no existe')
                return render_template('login.html', companies=companies)

            # Verificar contraseña
            if not user.verify_password(password):
                user.intentos_fallidos += 1
                db.session.commit()
                flash('Contraseña incorrecta.', 'error')
                logger.warning(f'Intento de login fallido: contraseña incorrecta para usuario {username}')
                return render_template('login.html', companies=companies)

            # Verificar si usuario está activo
            if not user.is_active():
                flash('Usuario inactivo. Contacte al administrador.', 'error')
                return render_template('login.html', companies=companies)

            # Verificar permisos para la compañía
            company = Compania.query.filter_by(codigo=company_code).first()
            if not company:
                flash('Compañía no encontrada.', 'error')
                return render_template('login.html', companies=companies)

            # Verificar permisos
            # permiso = user.permisos_compania.filter_by(compania_codigo=company_code).first()
            # if not permiso or not permiso.activo:
            #     flash('No tiene permisos para acceder a esta compañía.', 'error')
            #     return render_template('login.html', companies=companies)

            # Login exitoso
            login_user(user)

            # Actualizar información de login
            user.intentos_fallidos = 0
            user.ultimo_acceso = db.func.now()

            # Guardar compañía seleccionada en sesión
            session['empresa_actual'] = company_code
            g.empresa_actual = company

            # Crear registro de sesión
            nueva_sesion = SesionUsuario(
                usuario_id=user.id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', ''),
                activo=True
            )
            db.session.add(nueva_sesion)
            db.session.commit()

            logger.info(f'Login exitoso: usuario {username} en compañía {company_code}')

            # Redirigir al dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dashboard.index'))

        except Exception as e:
            db.session.rollback()
            logger.error(f'Error en login: {str(e)}')
            flash('Error interno del sistema. Intente nuevamente.', 'error')
            return render_template('login.html', companies=companies)

    # GET request - mostrar formulario
    try:
        # Obtener compañías activas (empre_actual = 1)
        companies = Compania.query.filter_by(activo=True).all()
        return render_template('login.html', companies=companies)
    except Exception as e:
        logger.error(f'Error cargando compañías: {str(e)}')
        flash('Error cargando lista de compañías.', 'error')
        return render_template('login.html', companies=[])

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    try:
        # Marcar sesión como inactiva
        if hasattr(current_user, 'sesiones'):
            sesion_activa = current_user.sesiones.filter_by(activo=True).first()
            if sesion_activa:
                sesion_activa.fecha_fin = db.func.now()
                sesion_activa.activo = False
                db.session.commit()

        logger.info(f'Logout: usuario {current_user.login}')
    except Exception as e:
        logger.error(f'Error en logout: {str(e)}')
    finally:
        logout_user()
        session.clear()

    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/cambiar-compania/<codigo>')
@login_required
def cambiar_compania(codigo):
    """Cambiar de compañía sin cerrar sesión"""
    try:
        # Verificar permisos para la nueva compañía
        permiso = current_user.permisos_compania.filter_by(
            compania_codigo=codigo,
            activo=True
        ).first()

        if not permiso:
            flash('No tiene permisos para acceder a esta compañía.', 'error')
            return redirect(request.referrer or url_for('dashboard.index'))

        # Actualizar compañía en sesión
        session['empresa_actual'] = codigo

        # Obtener datos de la nueva compañía
        company = Compania.query.filter_by(codigo=codigo).first()
        if company:
            g.empresa_actual = company

        flash(f'Compañía cambiada a: {company.nombre if company else codigo}', 'success')
        logger.info(f'Cambio de compañía: usuario {current_user.login} a {codigo}')

    except Exception as e:
        logger.error(f'Error cambiando compañía: {str(e)}')
        flash('Error cambiando de compañía.', 'error')

    return redirect(url_for('dashboard.index'))

@auth_bp.route('/perfil')
@login_required
def perfil():
    """Página de perfil de usuario"""
    return render_template('perfil.html')

@auth_bp.route('/cambiar-password', methods=['POST'])
@login_required
def cambiar_password():
    """Cambiar contraseña del usuario"""
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Validaciones
        if not current_password or not new_password or not confirm_password:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('auth.perfil'))

        if new_password != confirm_password:
            flash('Las contraseñas nuevas no coinciden.', 'error')
            return redirect(url_for('auth.perfil'))

        if len(new_password) < 6:
            flash('La nueva contraseña debe tener al menos 6 caracteres.', 'error')
            return redirect(url_for('auth.perfil'))

        # Verificar contraseña actual
        if not current_user.verify_password(current_password):
            flash('La contraseña actual es incorrecta.', 'error')
            return redirect(url_for('auth.perfil'))

        # Cambiar contraseña
        current_user.password = new_password
        db.session.commit()

        logger.info(f'Cambio de contraseña exitoso: usuario {current_user.login}')
        flash('Contraseña cambiada exitosamente.', 'success')

    except Exception as e:
        db.session.rollback()
        logger.error(f'Error cambiando contraseña: {str(e)}')
        flash('Error cambiando contraseña.', 'error')

    return redirect(url_for('auth.perfil'))

# Funciones auxiliares
def load_empresa_actual():
    """Carga la empresa actual desde la sesión"""
    if 'empresa_actual' in session and current_user.is_authenticated:
        try:
            company = Compania.query.filter_by(codigo=session['empresa_actual']).first()
            return company
        except Exception as e:
            logger.error(f'Error cargando empresa actual: {str(e)}')
    return None

# Registrar función en el contexto de la aplicación
def init_auth_context(app):
    """Inicializar contexto de autenticación"""
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            g.empresa_actual = load_empresa_actual()