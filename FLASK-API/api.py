print('Iniciando Servidor Flask...')

from flask import Flask # Serve para criar o servidor
from flask_sqlalchemy import SQLAlchemy # ORM (Mapa Objeto-Relacional) para interagir com o Banco de Dados usando objetos do Python

app = Flask(__name__) #Flask é uma classe que representa a aplicação web. // '__name__' é uma variável especial de scripts python.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) #80 caracteres
    email = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
         return f"User(name = {self.name}, email = {self.email})"

@app.route('/')
def home(): #homepage
        return '<h1>Flask REST API </h1>'
    
if __name__ == '__main__':
    app.run(debug=True)