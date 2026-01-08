from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.facturacion.models import FacturaCabecera, FacturaDetalle, Cliente, Vendedor, Producto, db
from sqlalchemy import and_, or_

facturacion_bp = Blueprint('facturacion', __name__, url_prefix='/facturacion')

@facturacion_bp.route('/facturas')
@login_required
def lista_facturas():
    # Obtener parámetros de filtro
    tipo = request.args.get('tipo', 'FAV')  # FAV, DEV, NDE
    buscar = request.args.get('buscar', '')
    fecha_desde = request.args.get('fecha_desde', '')
    fecha_hasta = request.args.get('fecha_hasta', '')

    # Query base con JOIN para búsqueda por cliente
    query = db.session.query(FacturaCabecera).join(Cliente, FacturaCabecera.cod_cliente == Cliente.codigo)

    # Filtrar por tipo (asumiendo que hay una columna para tipo, o filtrar por prefijo)
    # Por ahora, mostrar todas, pero en el futuro filtrar por tipo

    # Filtrar por búsqueda
    if buscar:
        query = query.filter(
            or_(
                FacturaCabecera.id.contains(buscar),
                FacturaCabecera.num_fiscal.contains(buscar),
                Cliente.nombre.contains(buscar)
            )
        )

    # Filtrar por fecha
    if fecha_desde and fecha_hasta:
        from datetime import datetime
        try:
            desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
            hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')
            query = query.filter(
                and_(
                    FacturaCabecera.fecha >= desde,
                    FacturaCabecera.fecha <= hasta
                )
            )
        except ValueError:
            flash('Formato de fecha inválido', 'warning')

    facturas = query.all()

    return render_template('facturacion/facturas.html', 
                         facturas=facturas, 
                         tipo=tipo, 
                         buscar=buscar, 
                         fecha_desde=fecha_desde, 
                         fecha_hasta=fecha_hasta)

@facturacion_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva_factura():
    """Página para crear nueva factura"""
    from datetime import datetime
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    if request.method == 'POST':
        # Procesar el formulario de nueva factura
        try:
            # Obtener datos del formulario
            tipo_documento = request.form.get('tipoDocumento')
            correlativo = request.form.get('correlativo')
            fecha = request.form.get('fecha')
            cod_cliente = request.form.get('codCliente')
            cod_vendedor = request.form.get('codVendedor')
            condicion_pago = request.form.get('condicionPago')
            plazo_dias = int(request.form.get('plazoDias', 0))
            divisa = request.form.get('divisa')
            descuento_general = float(request.form.get('descuentoGeneral', 0))

            # Crear nueva factura
            nueva_factura = FacturaCabecera(
                fecha=datetime.strptime(fecha, '%Y-%m-%d'),
                tipo=tipo_documento,
                cod_cliente=cod_cliente,
                cod_vendedor=cod_vendedor,
                condicion_pago=condicion_pago,
                plazo_dias=plazo_dias,
                divisa=divisa,
                descuento_general=descuento_general,
                usuario_creacion=current_user.username,
                fecha_creacion=datetime.now()
            )

            db.session.add(nueva_factura)
            db.session.commit()

            flash('Factura creada exitosamente', 'success')
            return redirect(url_for('facturacion.detalle_factura', id=nueva_factura.id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la factura: {str(e)}', 'error')
            return redirect(url_for('facturacion.nueva_factura'))

    return render_template('facturacion/nueva_factura.html', fecha_actual=fecha_actual)

@facturacion_bp.route('/api/test')
def api_test():
    """API de prueba simple"""
    return jsonify({'message': 'API funcionando', 'status': 'ok'})

@facturacion_bp.route('/api/clientes')
@login_required
def api_clientes():
    """API para obtener lista de clientes para el modal
    
    Equivalente a lbxClientes() en el código C#:
    - Consulta: SELECT cli_codigo,cli_nombre,cli_rif,cli_categoria,cli_situacion FROM admclientes LIMIT 45
    - Filtra por situacion = 'Activo'
    """
    # Obtener todos los clientes activos (equivalente a lbxClientes() LIMIT 45)
    clientes = Cliente.query.filter(Cliente.situacion == 'Activo').limit(45).all()
    
    # Convertir a formato JSON
    clientes_data = []
    for cliente in clientes:
        clientes_data.append({
            'codigo': cliente.codigo,
            'nombre': cliente.nombre.strip() if cliente.nombre else '',
            'rif': (cliente.rif or '').strip(),
            'categoria': (cliente.categoria or '').strip(),
            'situacion': (cliente.situacion or '').strip()
        })
    
    return jsonify({'clientes': clientes_data})

@facturacion_bp.route('/api/clientes/buscar')
@login_required
def api_buscar_clientes():
    """API para buscar clientes por código, nombre o RIF
    
    Equivalente a clienteBuscado() en el código C#:
    - Consulta: SELECT cli_codigo,cli_nombre,cli_rif,cli_categoria,cli_situacion 
                FROM admclientes WHERE cli_codigo LIKE '%$1%' OR cli_nombre LIKE '%$1%' OR cli_rif LIKE '%$1%'
    - Filtra por situacion = 'Activo'
    """
    termino = request.args.get('q', '').strip()
    
    if not termino:
        return jsonify({'clientes': []})
    
    # Buscar clientes que coincidan con el término (equivalente a clienteBuscado())
    clientes = Cliente.query.filter(
        or_(
            Cliente.codigo.contains(termino),
            Cliente.nombre.contains(termino),
            Cliente.rif.contains(termino)
        )
    ).filter(Cliente.situacion == 'Activo').limit(50).all()
    
    # Convertir a formato JSON
    clientes_data = []
    for cliente in clientes:
        clientes_data.append({
            'codigo': cliente.codigo,
            'nombre': cliente.nombre.strip() if cliente.nombre else '',
            'rif': (cliente.rif or '').strip(),
            'categoria': (cliente.categoria or '').strip(),
            'situacion': (cliente.situacion or '').strip()
        })
    
    return jsonify({'clientes': clientes_data})

# @facturacion_bp.route('/api/clientes/buscar')
# # @login_required  # Temporalmente comentado para pruebas
# def api_buscar_clientes():
#     """API para buscar clientes por código, nombre o RIF
#     
#     Equivalente a clienteBuscado() en el código C#:
#     - Consulta: SELECT cli_codigo,cli_nombre,cli_rif,cli_categoria,cli_situacion 
#                 FROM admclientes WHERE cli_codigo LIKE '%$1%' OR cli_nombre LIKE '%$1%' OR cli_rif LIKE '%$1%'
#     - Filtra por situacion = 'Activo'
#     """
#     termino = request.args.get('q', '').strip()
#     
#     if not termino:
#         return jsonify({'clientes': []})
#     
#     # Buscar clientes que coincidan con el término (equivalente a clienteBuscado())
#     clientes = Cliente.query.filter(
#         or_(
#             Cliente.codigo.contains(termino),
#             Cliente.nombre.contains(termino),
#             Cliente.rif.contains(termino)
#         )
#     ).filter(Cliente.situacion == 'Activo').limit(50).all()
#     
#     # Convertir a formato JSON
#     clientes_data = []
#     for cliente in clientes:
#         clientes_data.append({
#             'codigo': cliente.codigo,
#             'nombre': cliente.nombre.strip() if cliente.nombre else '',
#             'rif': (cliente.rif or '').strip(),
#             'categoria': (cliente.categoria or '').strip(),
#             'situacion': (cliente.situacion or '').strip()
#         })
#     
#     return jsonify({'clientes': clientes_data})

@facturacion_bp.route('/factura/<int:id>')
@login_required
def detalle_factura(id):
    """Ver detalles de una factura específica"""
    factura = FacturaCabecera.query.get_or_404(id)
    return render_template('facturacion/detalle_factura.html', factura=factura)
