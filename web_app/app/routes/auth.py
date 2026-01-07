from flask import Blueprint, render_template, redirect, url_for, flash, request, session, g
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import db, UsuarioSistema, Compania, PermisoCompania, SesionUsuario
from app.menu import cargar_menu_usuario
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Vista de login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        company_code = request.form.get('company', '').strip()

        if not username or not password:
            flash('Por favor ingrese usuario y contraseña.', 'warning')
            return render_template('login.html')

        try:
            # Buscar usuario
            usuario = UsuarioSistema.query.filter_by(login=username).first()

            if not usuario:
                flash('Usuario o contraseña incorrectos.', 'danger')
                logger.warning(f'Intento de login fallido: usuario {username} no existe')
                return render_template('login.html')

            # Verificar si usuario está activo
            if not usuario.is_active():
                flash('Usuario inactivo. Contacte al administrador.', 'danger')
                logger.warning(f'Intento de login con usuario inactivo: {username}')
                return render_template('login.html')

            # Verificar contraseña
            if not usuario.verify_password(password):
                # Incrementar contador de intentos fallidos
                usuario.intentos_fallidos = (usuario.intentos_fallidos or 0) + 1
                db.session.commit()

                flash('Usuario o contraseña incorrectos.', 'danger')
                logger.warning(f'Contraseña incorrecta para usuario: {username}')
                return render_template('login.html')

            # Verificar permisos de compañía si se especificó una
            if company_code:
                permiso = PermisoCompania.query.filter_by(
                    usuario_id=usuario.id,
                    compania_codigo=company_code,
                    activo=True
                ).first()

                if not permiso:
                    flash('No tiene permisos para acceder a esta compañía.', 'danger')
                    logger.warning(f'Usuario {username} sin permisos para compañía {company_code}')
                    return render_template('login.html')

                # Obtener datos de la compañía
                compania = Compania.query.filter_by(codigo=company_code).first()
                if not compania or not compania.activo:
                    flash('Compañía no válida o inactiva.', 'danger')
                    return render_template('login.html')

                session['empresa_actual'] = {
                    'codigo': compania.codigo,
                    'nombre': compania.nombre,
                    'rif': compania.rif
                }
            else:
                # Si no se especificó compañía, buscar la compañía por defecto
                permiso_default = PermisoCompania.query.filter_by(
                    usuario_id=usuario.id,
                    activo=True
                ).first()

                if permiso_default:
                    compania = Compania.query.filter_by(codigo=permiso_default.compania_codigo).first()
                    if compania and compania.activo:
                        session['empresa_actual'] = {
                            'codigo': compania.codigo,
                            'nombre': compania.nombre,
                            'rif': compania.rif
                        }

            # Resetear intentos fallidos
            usuario.intentos_fallidos = 0
            usuario.ultimo_acceso = datetime.utcnow()
            db.session.commit()

            # Crear sesión
            token_sesion = str(uuid.uuid4())
            nueva_sesion = SesionUsuario(
                usuario_id=usuario.id,
                token_sesion=token_sesion,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                activo=True
            )
            db.session.add(nueva_sesion)
            db.session.commit()

            session['session_token'] = token_sesion

            # Cargar menú del usuario
            menu_data = cargar_menu_usuario(usuario.id, 'Ventas')
            session['menu_data'] = menu_data

            # Login exitoso
            login_user(usuario, remember=True)
            logger.info(f'Login exitoso: {username}')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dashboard.index'))

        except Exception as e:
            db.session.rollback()
            logger.error(f'Error en login: {str(e)}')
            flash('Error interno del sistema. Intente nuevamente.', 'danger')
            return render_template('login.html')

    # GET request - mostrar formulario de login
    try:
        # Obtener compañías activas (empre_actual = 1)
        companies = Compania.query.filter_by(activo=True).all()
        return render_template('login.html', companies=companies)
    except Exception as e:
        logger.error(f'Error cargando compañías: {str(e)}')
        flash('Error cargando datos de compañías.', 'warning')
        return render_template('login.html', companies=[])

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    try:
        # Marcar sesión como inactiva
        if 'session_token' in session:
            sesion = SesionUsuario.query.filter_by(
                token_sesion=session['session_token'],
                activo=True
            ).first()

            if sesion:
                sesion.fecha_fin = datetime.utcnow()
                sesion.activo = False
                db.session.commit()

        # Limpiar sesión
        session.clear()

        # Logout de Flask-Login
        logout_user()

        logger.info(f'Logout exitoso: {current_user.login if current_user.is_authenticated else "usuario desconocido"}')

    except Exception as e:
        logger.error(f'Error en logout: {str(e)}')

    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/companies')
def get_companies():
    """API para obtener compañías (para AJAX)"""
    try:
        companies = Compania.query.filter_by(activo=True).all()
        return {
            'success': True,
            'companies': [
                {
                    'codigo': c.codigo,
                    'nombre': c.nombre,
                    'rif': c.rif
                } for c in companies
            ]
        }
    except Exception as e:
        logger.error(f'Error obteniendo compañías: {str(e)}')
        return {'success': False, 'error': 'Error interno del servidor'}, 500

@auth_bp.route('/check-session')
@login_required
def check_session():
    """Verificar estado de la sesión"""
    return {
        'authenticated': True,
        'user': {
            'id': current_user.id,
            'login': current_user.login,
            'nombre': current_user.nombre
        },
        'empresa': session.get('empresa_actual'),
        'timestamp': datetime.utcnow().isoformat()
    }