"""
Sistema de menús dinámicos para Lebrun Facturación Web
"""
import logging
from typing import Dict, List, Any
from flask import g

from app.models import MenuItem, MapaMenu

logger = logging.getLogger(__name__)

class MenuManager:
    """Administrador de menús dinámicos"""

    # Iconos por defecto para cada módulo
    DEFAULT_ICONS = {
        'Ventas': 'fas fa-shopping-cart',
        'Transacciones': 'fas fa-exchange-alt',
        'Procesos': 'fas fa-cogs',
        'Otros': 'fas fa-ellipsis-h'
    }

    # Iconos específicos para formularios
    FORM_ICONS = {
        'Factura de Venta': 'fas fa-file-invoice-dollar',
        'Devolucion de Venta': 'fas fa-undo',
        'Nota de Debito': 'fas fa-plus-circle',
        'Reporte X': 'fas fa-chart-bar',
        'Reporte Z': 'fas fa-chart-line',
        'Pedido': 'fas fa-clipboard-list',
        'Visor de Precios': 'fas fa-eye',
        'Visor2': 'fas fa-eye'
    }

    @staticmethod
    def get_menu_data(user_id: int, modulo: str = 'Ventas') -> Dict[str, Any]:
        """
        Obtiene los datos del menú para un usuario y módulo específico

        Args:
            user_id: ID del usuario
            modulo: Módulo del menú (Ventas, Inventario, etc.)

        Returns:
            Diccionario con la estructura del menú
        """
        try:
            # Obtener mapa de menú del usuario
            mapa_menu = MapaMenu.query.filter_by(
                codigo=str(user_id),
                modulo=modulo,
                activo=True
            ).first()

            if not mapa_menu:
                logger.warning(f'No se encontró mapa de menú para usuario {user_id} en módulo {modulo}')
                return {}

            # Obtener items del menú
            menu_items = MenuItem.query.filter_by(
                padre=modulo,
                activo=True
            ).order_by(MenuItem.orden).all()

            # Construir estructura jerárquica
            menu_data = MenuManager._build_menu_structure(menu_items, mapa_menu)

            return menu_data

        except Exception as e:
            logger.error(f'Error obteniendo menú para usuario {user_id}: {str(e)}')
            return {}

    @staticmethod
    def _build_menu_structure(menu_items: List[MenuItem], mapa_menu: MapaMenu) -> Dict[str, Any]:
        """
        Construye la estructura jerárquica del menú

        Args:
            menu_items: Lista de items del menú
            mapa_menu: Mapa de menú del usuario

        Returns:
            Estructura jerárquica del menú
        """
        menu_structure = {}

        for item in menu_items:
            # Verificar si el usuario tiene acceso a este item
            if not MenuManager._user_has_access(item, mapa_menu):
                continue

            padre_key = item.padre
            subpadre_key = item.subpadre or 'General'
            hijo_key = item.hijo

            # Inicializar padre si no existe
            if padre_key not in menu_structure:
                menu_structure[padre_key] = {
                    'icono': MenuManager.DEFAULT_ICONS.get(padre_key, 'fas fa-folder'),
                    'submenus': {}
                }

            # Inicializar subpadre si no existe
            if subpadre_key not in menu_structure[padre_key]['submenus']:
                menu_structure[padre_key]['submenus'][subpadre_key] = {
                    'icono': MenuManager.DEFAULT_ICONS.get(subpadre_key, 'fas fa-folder-open'),
                    'items': []
                }

            # Agregar item hijo
            menu_item = {
                'titulo': hijo_key,
                'ruta': item.ruta or f'#{hijo_key.lower().replace(" ", "_")}',
                'icono': MenuManager.FORM_ICONS.get(hijo_key, 'fas fa-file'),
                'descripcion': item.nombre or hijo_key,
                'tag': item.ruta
            }

            menu_structure[padre_key]['submenus'][subpadre_key]['items'].append(menu_item)

        return menu_structure

    @staticmethod
    def _user_has_access(menu_item: MenuItem, mapa_menu: MapaMenu) -> bool:
        """
        Verifica si el usuario tiene acceso a un item del menú

        Args:
            menu_item: Item del menú
            mapa_menu: Mapa de menú del usuario

        Returns:
            True si tiene acceso, False en caso contrario
        """
        # Por ahora, permitir acceso a todos los items
        # En el futuro, implementar lógica de permisos más granular
        return True

    @staticmethod
    def get_breadcrumb_data(menu_data: Dict[str, Any], current_path: str) -> List[Dict[str, str]]:
        """
        Genera datos para breadcrumb basado en la ruta actual

        Args:
            menu_data: Datos del menú
            current_path: Ruta actual

        Returns:
            Lista de elementos del breadcrumb
        """
        breadcrumbs = []

        # Buscar el item actual en la estructura del menú
        for padre_key, padre_data in menu_data.items():
            for subpadre_key, subpadre_data in padre_data.get('submenus', {}).items():
                for item in subpadre_data.get('items', []):
                    if item['ruta'] == current_path:
                        breadcrumbs = [
                            {'titulo': padre_key, 'ruta': '#', 'icono': padre_data['icono']},
                            {'titulo': subpadre_key, 'ruta': '#', 'icono': subpadre_data['icono']},
                            {'titulo': item['titulo'], 'ruta': item['ruta'], 'icono': item['icono']}
                        ]
                        break

        return breadcrumbs

    @staticmethod
    def get_quick_actions(user_id: int) -> List[Dict[str, str]]:
        """
        Obtiene acciones rápidas disponibles para el usuario

        Args:
            user_id: ID del usuario

        Returns:
            Lista de acciones rápidas
        """
        quick_actions = [
            {
                'titulo': 'Nueva Factura',
                'ruta': '/facturacion/nueva',
                'icono': 'fas fa-plus-circle',
                'color': 'primary',
                'descripcion': 'Crear nueva factura de venta'
            },
            {
                'titulo': 'Nuevo Cliente',
                'ruta': '/clientes/nuevo',
                'icono': 'fas fa-user-plus',
                'color': 'success',
                'descripcion': 'Registrar nuevo cliente'
            },
            {
                'titulo': 'Ver Reportes',
                'ruta': '/reportes',
                'icono': 'fas fa-chart-bar',
                'color': 'info',
                'descripcion': 'Consultar reportes del sistema'
            }
        ]

        return quick_actions

# Funciones de utilidad para templates
def get_menu_data():
    """Función para templates: obtiene datos del menú del usuario actual"""
    from flask_login import current_user

    if not current_user.is_authenticated:
        return {}

    return MenuManager.get_menu_data(current_user.id)

def get_breadcrumbs(current_path: str):
    """Función para templates: obtiene breadcrumb para la ruta actual"""
    menu_data = get_menu_data()
    return MenuManager.get_breadcrumb_data(menu_data, current_path)

def get_quick_actions():
    """Función para templates: obtiene acciones rápidas"""
    from flask_login import current_user

    if not current_user.is_authenticated:
        return []

    return MenuManager.get_quick_actions(current_user.id)

# Funciones de compatibilidad con la implementación anterior
def cargar_menu_usuario(usuario_id: int, modulo: str = 'Ventas') -> Dict:
    """
    Función de compatibilidad: carga el menú dinámico para un usuario específico
    """
    return MenuManager.get_menu_data(usuario_id, modulo)

def filtrar_menu_por_permisos(menu_data: Dict, permisos: List[str]) -> Dict:
    """
    Función de compatibilidad: filtra el menú según los permisos del usuario
    """
    # Por ahora, devolver el menú sin filtrar
    return menu_data

def generar_menu_html(menu_data: Dict, activo: str = None) -> str:
    """
    Función de compatibilidad: genera HTML para el menú lateral
    """
    if not menu_data:
        return '<div class="alert alert-warning">No hay elementos de menú disponibles</div>'

    html = '<nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">\n'
    html += '  <div class="container-fluid">\n'
    html += '    <a class="navbar-brand" href="#">Lebrun Facturación</a>\n'
    html += '    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">\n'
    html += '      <span class="navbar-toggler-icon"></span>\n'
    html += '    </button>\n'
    html += '    <div class="collapse navbar-collapse" id="navbarNav">\n'
    html += '      <ul class="navbar-nav me-auto">\n'

    for padre_key, padre_data in menu_data.items():
        html += f'        <li class="nav-item dropdown">\n'
        html += f'          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">\n'
        html += f'            <i class="{padre_data["icono"]}"></i> {padre_key}\n'
        html += '          </a>\n'
        html += '          <ul class="dropdown-menu">\n'

        for subpadre_key, subpadre_data in padre_data['submenus'].items():
            if subpadre_data['items']:
                html += f'            <li class="dropdown-submenu">\n'
                html += f'              <a class="dropdown-item" href="#">\n'
                html += f'                <i class="{subpadre_data["icono"]}"></i> {subpadre_key}\n'
                html += '              </a>\n'
                html += '              <ul class="dropdown-menu submenu">\n'

                for item in subpadre_data['items']:
                    active_class = ' active' if activo and activo in item['titulo'] else ''
                    html += f'                <li>\n'
                    html += f'                  <a class="dropdown-item{active_class}" href="{item["ruta"]}">\n'
                    html += f'                    <i class="{item["icono"]}"></i> {item["titulo"]}\n'
                    html += '                  </a>\n'
                    html += '                </li>\n'

                html += '              </ul>\n'
                html += '            </li>\n'

        html += '          </ul>\n'
        html += '        </li>\n'

    html += '      </ul>\n'
    html += '      <ul class="navbar-nav">\n'
    html += '        <li class="nav-item dropdown">\n'
    html += '          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">\n'
    html += '            <i class="fas fa-user"></i> Usuario\n'
    html += '          </a>\n'
    html += '          <ul class="dropdown-menu">\n'
    html += '            <li><a class="dropdown-item" href="#"><i class="fas fa-user-cog"></i> Perfil</a></li>\n'
    html += '            <li><a class="dropdown-item" href="#"><i class="fas fa-cog"></i> Configuración</a></li>\n'
    html += '            <li><hr class="dropdown-divider"></li>\n'
    html += '            <li><a class="dropdown-item" href="/auth/logout"><i class="fas fa-sign-out-alt"></i> Cerrar Sesión</a></li>\n'
    html += '          </ul>\n'
    html += '        </li>\n'
    html += '      </ul>\n'
    html += '    </div>\n'
    html += '  </div>\n'
    html += '</nav>\n'

    return html

def obtener_rutas_menu(menu_data: Dict) -> List[str]:
    """
    Función de compatibilidad: obtiene todas las rutas disponibles en el menú
    """
    rutas = []

    for padre_data in menu_data.values():
        for subpadre_data in padre_data['submenus'].values():
            for item in subpadre_data['items']:
                rutas.append(item['ruta'])

    return rutas