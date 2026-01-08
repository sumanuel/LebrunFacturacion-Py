from app.models import db

class Cliente(db.Model):
    """Modelo para clientes"""
    __tablename__ = 'admclientes'
    __bind_key__ = 'sisadm'

    codigo = db.Column('cli_codigo', db.String(20), primary_key=True)
    nombre = db.Column('cli_nombre', db.String(100), nullable=False)
    rif = db.Column('cli_rif', db.String(20))
    telefono = db.Column('cli_telefono', db.String(20))
    categoria = db.Column('cli_categoria', db.String(50))
    situacion = db.Column('cli_situacion', db.String(20))

    def __repr__(self):
        return f'<Cliente {self.nombre}>'

class Vendedor(db.Model):
    """Modelo para vendedores"""
    __tablename__ = 'admvendedores'
    __bind_key__ = 'sisadm'

    codigo = db.Column('ven_codigo', db.String(10), primary_key=True)
    nombre = db.Column('ven_nombre', db.String(100), nullable=False)

    def __repr__(self):
        return f'<Vendedor {self.nombre}>'

class Producto(db.Model):
    """Modelo para productos"""
    __tablename__ = 'admproductos'
    __bind_key__ = 'sisadm'

    codigo = db.Column('pro_codigo', db.String(20), primary_key=True)
    nombre = db.Column('pro_nombre', db.String(100), nullable=False)
    unidad = db.Column('pro_unidad', db.String(10))
    precio = db.Column('pro_precio', db.Float, default=0.0)
    stock = db.Column('pro_stock', db.Float, default=0.0)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

class FacturaCabecera(db.Model):
    """Modelo para cabeceras de facturas"""
    __tablename__ = 'admdoccli'
    __bind_key__ = 'sisadm'

    id = db.Column('dcli_numero', db.String(20), primary_key=True)
    fecha = db.Column('dcli_fecha', db.DateTime)
    tipo = db.Column('dcli_tipdoc', db.String(10))  # FAV, DEV, NDE
    cod_cliente = db.Column('dcli_codigo', db.String(20))
    cod_vendedor = db.Column('dcli_codven', db.String(10))
    condicion_pago = db.Column('dcli_condic', db.String(20))  # CONTADO, CREDITO
    plazo_dias = db.Column('dcli_plazo', db.Integer, default=0)
    divisa = db.Column('dcli_codmon', db.String(10), default='VES')
    descuento_general = db.Column('dcli_descdoc', db.Float, default=0.0)
    subtotal = db.Column('dcli_subtotal', db.Float, default=0.0)
    iva = db.Column('dcli_mtoiva', db.Float, default=0.0)
    total = db.Column('dcli_neto', db.Float, default=0.0)
    estado = db.Column('dcli_estado', db.String(20), default='ACTIVA')
    num_fiscal = db.Column('dcli_numfis', db.String(20))
    usuario_creacion = db.Column('dcli_usuario', db.String(50))

    # Relationships
    cliente = db.relationship('Cliente', foreign_keys=[cod_cliente], primaryjoin="FacturaCabecera.cod_cliente == Cliente.codigo", lazy='select')
    vendedor = db.relationship('Vendedor', foreign_keys=[cod_vendedor], primaryjoin="FacturaCabecera.cod_vendedor == Vendedor.codigo", lazy='select')
    detalles = db.relationship('FacturaDetalle', back_populates='factura', lazy='select')

    def __repr__(self):
        return f'<Factura {self.id}>'

class FacturaDetalle(db.Model):
    """Modelo para detalles de facturas"""
    __tablename__ = 'admdocclid'
    __bind_key__ = 'sisadm'

    id = db.Column('dclid_numero', db.String(20), primary_key=True)
    linea = db.Column('dclid_linea', db.Integer, primary_key=True)
    cod_producto = db.Column('dclid_codigo', db.String(20))
    descripcion = db.Column('dclid_descripcion', db.String(100))
    unidad = db.Column('dclid_unidad', db.String(10))
    cantidad = db.Column('dclid_cantidad', db.Float, default=0.0)
    precio = db.Column('dclid_precio', db.Float, default=0.0)
    descuento = db.Column('dclid_descuento', db.Float, default=0.0)
    total = db.Column('dclid_total', db.Float, default=0.0)

    # Relationship con factura
    factura = db.relationship('FacturaCabecera', back_populates='detalles')
    # Foreign key constraint
    __table_args__ = (
        db.ForeignKeyConstraint([id], [FacturaCabecera.id]),
    )

    # Relationship con producto
    producto = db.relationship('Producto', foreign_keys=[cod_producto], primaryjoin="FacturaDetalle.cod_producto == Producto.codigo", lazy='select')

    def __repr__(self):
        return f'<FacturaDetalle {self.id}-{self.linea}>'