from app import db, app, User  # Cria o banco de dados e as tabelas

with app.app_context():
    db.create_all()
    print("Banco criado com as tabelas!")
