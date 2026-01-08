from app.models import db

class Cliente(db.Model):
    """Modelo para clientes"""
    __tablename__ = 'admclientes'
    __bind_key__ = 'sisadm'

    codigo = db.Column('cli_codigo', db.String(20), primary_key=True)
    nombre = db.Column('cli_nombre', db.String(100), nullable=False)
    rif = db.Column('cli_rif', db.String(20))

    def __repr__(self):
        return f'<Cliente {self.nombre}>'

class FacturaCabecera(db.Model):
    """Modelo para cabeceras de facturas"""
    __tablename__ = 'admdoccli'
    __bind_key__ = 'sisadm'

    id = db.Column('dcli_numero', db.String(20), primary_key=True)
    codigo_cliente = db.Column('dcli_codigo', db.String(20))
    fecha = db.Column('dcli_fecha', db.DateTime)
    estado = db.Column('dcli_estado', db.String(20))
    monto = db.Column('dcli_neto', db.Float)
    num_fiscal = db.Column('dcli_numfis', db.String(20))
    imp = db.Column('dcli_mtoiva', db.Float)

    # Relationship con cliente
    cliente = db.relationship('Cliente', foreign_keys=[codigo_cliente], primaryjoin="FacturaCabecera.codigo_cliente == Cliente.codigo", lazy='joined')