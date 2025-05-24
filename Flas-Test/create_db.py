from app import app, db # Importando o app e db do módulo app

with app.app_context():
    db.create_all()
    print("Banco criado com as tabelas!")
