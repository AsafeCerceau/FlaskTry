from flask import Flask  # Serve para criar o servidor
print('\nIniciando Servidor Flask...\n')
from flask_restful import Api

# ORM (Mapa Objeto-Relacional) para interagir com o Banco de Dados usando objetos do Python
from models import db  # Importa o objeto db do módulo models
from routes.user_routes import Users, User  # Importa as classes Users e User definidas em outro arquivo


# Flask é um microframework para Python que permite criar aplicações web de forma simples e rápida.

# Flask é uma classe que representa a aplicação web. // '__name__' é uma variável especial de scripts python.
app = Flask(__name__)
# Define a URL de conexão com o banco de dados // 'sqlite:///database.db' quer dizer que o banco será salvo como um arquivo local chamado 'database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)  # Inicializa o banco de dados com a aplicação Flask
api = Api(app)  # Cria uma instância da API RESTful usando a aplicação Flask


# Rotas da API
api.add_resource(Users, '/api/users')  # Adiciona a classe Users como um recurso na API, acessível pela rota '/users'
api.add_resource(User, '/api/users/<int:id>')  # Adiciona a classe User como um recurso na API, acessível pela rota '/users/<id>'

@app.route('/')  # Define a rota '/' (ou seja, a página principal)
def home():  # homepage // Quanto o navegador acessar 'localhost:5000/', essa função será chamada
    return '<h1>Flask REST API </h1>'  # Retorna HTML simples

if __name__ == '__main__':  # Garante que o servidor Flask só será executado se este arquivo for o principal (e não importado por outro)
    app.run(debug=True)  # Ativa o modo de desenvolvimento: atualização automática ao salvar & exibe erros detalhados no navegador.