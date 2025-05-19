from models import db  # Importa o objeto db do módulo models

class UserModel(db.Model):
    __tablename__ = 'Usuários:'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nome de usuário único
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único
    password = db.Column(db.String(200), nullable=False)  # Senha

    def __repr__(self):
        return f'<User {self.username}>'