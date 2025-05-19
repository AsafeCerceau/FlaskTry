from flask import Flask  # Serve para criar o servidor
print('Iniciando Servidor Flask...')
# Serve para criar APIs RESTful
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

# ORM (Mapa Objeto-Relacional) para interagir com o Banco de Dados usando objetos do Python
from models import db  # Importa o objeto db do módulo models
from models.user_model import UserModel  # Importa o modelo de usuário definido em outro arquivo


# Flask é um microframework para Python que permite criar aplicações web de forma simples e rápida.

# Flask é uma classe que representa a aplicação web. // '__name__' é uma variável especial de scripts python.
app = Flask(__name__)
# Define a URL de conexão com o banco de dados // 'sqlite:///database.db' quer dizer que o banco será salvo como um arquivo local chamado 'database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)  # Inicializa o banco de dados com a aplicação Flask

api = Api(app)  # Cria uma instância da API RESTful usando a aplicação Flask
# O SQLAlchemy é uma biblioteca ORM (Object Relational Mapper) que facilita a interação com bancos de dados relacionais, permitindo que você trabalhe com objetos Python em vez de escrever consultas SQL diretamente.


# Cria um parser de argumentos para a requisição
user_args = reqparse.RequestParser()
# Adiciona um argumento 'name' do tipo string, obrigatório e com mensagem de erro se estiver em branco
user_args.add_argument('name', type=str, required=True,
                       help='Name cannot be blank')
# Adiciona um argumento 'email' do tipo string, obrigatório e com mensagem de erro se estiver em branco
user_args.add_argument('email', type=str, required=True,
                       help='Email cannot be blank')

userFields = {  # Define os campos que serão retornados na resposta da API
    'id': fields.Integer,  # Campo 'id' do tipo inteiro
    'name': fields.String,  # Campo 'name' do tipo string
    'email': fields.String,  # Campo 'email' do tipo string
}


class Users(Resource):  # Cria uma classe 'Users' que herda de 'Resource' (do Flask-RESTful)
    # Decora o método com 'marshal_with' para formatar a resposta com os campos definidos em 'userFields'
    @marshal_with(userFields)
    def get(self):  # Método GET para obter todos os usuários
        # Faz uma consulta no banco de dados para obter todos os usuários
        users = UserModel.query.all()
        return users  # Retorna a lista de usuários

    # Decora o método com 'marshal_with' para formatar a resposta com os campos definidos em 'userFields'
    @marshal_with(userFields)
    def post(self):  # Método POST para criar um novo usuário
        # Analisa os argumentos da requisição // 'args' é um dicionário com os argumentos analisados //
        args = user_args.parse_args()
        # Cria um novo usuário com os dados fornecidos
        user = UserModel(name=args['name'], email=args['email'])
        # Adiciona o novo usuário à sessão do banco de dados
        db.session.add(user)
        db.session.commit()
        # Faz uma consulta no banco de dados para obter todos os usuários
        users = UserModel.query.all()
        # Retorna a lista de usuários e o código de status 201 (Criado)
        return users, 201


class User(Resource):  # Cria uma classe 'User' que herda de 'Resource'
    @marshal_with(userFields)
    def get(self, id):  # Método GET para obter um usuário específico
        # Faz uma consulta no banco de dados para obter o usuário com o ID fornecido
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            # Se o usuário não for encontrado, retorna um erro 404
            abort(404, message="Usuário não encontrado.")
        return user  # Retorna o usuário encontrado

    @marshal_with(userFields)
    def patch(self, id):  # Método PATCH para atualizar um usuário específico
        args = user_args.parse_args()  # Analisa os argumentos da requisição
        # Faz uma consulta no banco de dados para obter o usuário com o ID fornecido
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            # Se o usuário não for encontrado, retorna um erro 404
            abort(404, message="Usuário não encontrado.")
        user.name = args['name']  # Atualiza o nome do usuário
        user.email = args['email']  # Atualiza o email do usuário
        db.session.commit()  # Salva as alterações no banco de dados
        # Faz uma consulta no banco de dados para obter o usuário atualizado
        return user  # Retorna o usuário encontrado/atualizado

# Método DELETE para excluir um usuário específico
    @marshal_with(userFields)
    def delete(self, id):  # Método PATCH para atualizar um usuário específico
        # Faz uma consulta no banco de dados para obter o usuário com o ID fornecido
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            # Se o usuário não for encontrado, retorna um erro 404
            abort(404, message="Usuário não encontrado.")
        db.session.delete(user)  # Exclui o usuário do banco de dados
        db.session.commit()  # Salva as alterações no banco de dados
        users = UserModel.query.all()
        return users


# Adiciona a classe 'Users' como um recurso na API, acessível pela rota '/users'
api.add_resource(Users, '/api/users')
# Adiciona a classe 'User' como um recurso na API, acessível pela rota '/users/<id>'
api.add_resource(User, '/api/users/<int:id>')


# O Flask-RESTful é uma extensão do Flask que facilita a criação de APIs RESTful, fornecendo classes e métodos para lidar com requisições HTTP de forma mais simples.
# O reqparse é uma ferramenta do Flask-RESTful que permite analisar e validar os argumentos da requisição, facilitando o tratamento de dados enviados pelo cliente.

@app.route('/')  # define a rota '/' (ou seja, a página principal)
def home():  # homepage // Quanto o navegador acessar 'localhost:5000/', essa fundão será chamada
    return '<h1>Flask REST API </h1>'  # retorna HTML simples


# Garante que o servidor Flask só será executado se este arquivo for o princpal (e não importado por outro)
if __name__ == '__main__':
    # ativa o modo de desenvolvimento: atualização automática ao salvar & exibe erros detalhados no navegador.
    app.run(debug=True)