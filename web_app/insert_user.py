from application import create_app, db
from sqlalchemy import text
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    engine_sisadm = db.engines['sisadm']
    with engine_sisadm.connect() as conn:
        # Generar hash para 'admin'
        hashed = generate_password_hash('admin')
        conn.execute(text(f"INSERT INTO confusuarios (usu_login, usu_password, usu_nombre, usu_activo) VALUES ('admin', '{hashed}', 'Administrador', 1)"))
        conn.commit()
        print('Usuario admin insertado con hash:', hashed)