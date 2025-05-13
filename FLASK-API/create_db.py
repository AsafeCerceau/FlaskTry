from api import app, db

with app.app_context():  # Cria um contexto de aplicativo Flask
    # Cria o banco de dados e as tabelas
    db.create_all()  # Cria todas as tabelas definidas nos modelos do banco de dados
