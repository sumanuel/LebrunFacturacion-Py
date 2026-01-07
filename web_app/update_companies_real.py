#!/usr/bin/env python3
"""
Script para actualizar las compañías en la base de datos web
con los datos reales de confdatosempresa
"""

from app.models import Compania, db
from application import create_app

def update_companies():
    """Actualizar compañías con datos reales"""
    app = create_app()
    with app.app_context():
        # Datos de las compañías reales
        companies_data = [
            {
                "nombre": "Ferreteria Lebrun",
                "codigo": "01",
                "activo": True
            },
            {
                "nombre": "Ferreteria El Timon",
                "codigo": "02",
                "activo": False
            },
            {
                "nombre": "La Tienda del Carpintero",
                "codigo": "03",
                "activo": False
            },
            {
                "nombre": "Ferreteria Brunle",
                "codigo": "04",
                "activo": False
            },
            {
                "nombre": "Ferrecarpi",
                "codigo": "05",
                "activo": False
            },
            {
                "nombre": "Ferreteria Ferresama",
                "codigo": "06",
                "activo": False
            }
        ]

        # Limpiar compañías existentes
        Compania.query.delete()
        db.session.commit()

        # Insertar compañías actualizadas
        for company_data in companies_data:
            company = Compania(
                nombre=company_data["nombre"],
                codigo=company_data["codigo"],
                activo=company_data["activo"],
                rif="J-123456789" if company_data["codigo"] == "01" else None  # Mantener RIF para Lebrun
            )
            db.session.add(company)

        db.session.commit()
        print("Compañías actualizadas correctamente")

        # Verificar
        companies = Compania.query.all()
        print("Compañías en DB:")
        for c in companies:
            print(f"- {c.nombre} (código: {c.codigo}, activo: {c.activo})")

if __name__ == "__main__":
    update_companies()