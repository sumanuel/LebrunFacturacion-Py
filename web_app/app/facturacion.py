from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import FacturaCabecera, Cliente, db
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

    # Query base
    query = FacturaCabecera.query

    # Filtrar por tipo (asumiendo que hay una columna para tipo, o filtrar por prefijo)
    # Por ahora, mostrar todas, pero en el futuro filtrar por tipo

    # Filtrar por búsqueda
    if buscar:
        query = query.filter(
            or_(
                FacturaCabecera.id.contains(buscar),
                FacturaCabecera.cliente.has(Cliente.nombre.contains(buscar)),
                FacturaCabecera.num_fiscal.contains(buscar)
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

    return render_template('facturas.html', 
                         facturas=facturas,
                         tipo=tipo,
                         buscar=buscar,
                         fecha_desde=fecha_desde,
                         fecha_hasta=fecha_hasta)