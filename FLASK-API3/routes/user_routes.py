from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort # Importa as classes necessárias do Flask-RESTful
from models.user_model import UserModel # Importa o modelo de usuário definido em outro arquivo
from models import db # Importa o objeto db do módulo models

#cria um parser de argumentos para a entrada de dados
user_args = reqparse.RequestParser() # Cria um parser de argumentos para a requisição
user_args.add_argument('nome', type=str, required=True, help='Nome não pode ser vazio') # Adiciona um argumento 'name' do tipo string, obrigatório e com mensagem de erro se estiver em branco
user_args.add_argument('email', type=str, required=True, help='Email não pode ser vazio') # Adiciona um argumento 'email' do tipo string, obrigatório e com mensagem de erro se estiver em branco


userFields = { # Define os campos que serão retornados na resposta da API
    'id': fields.Integer, # Campo 'id' do tipo inteiro
    'nome': fields.String, # Campo 'name' do tipo string
    'email': fields.String, # Campo 'email' do tipo string
}

class Users(Resource): # Cria uma classe 'Users' que herda de 'Resource' (do Flask-RESTful)
    @marshal_with(userFields) # Decora o método com 'marshal_with' para formatar a resposta com os campos definidos em 'userFields'
    def get(self): # Método GET para obter todos os usuários
        users = UserModel.query.all() # Faz uma consulta no banco de dados para obter todos os usuários
        return users # Retorna a lista de usuários

    @marshal_with(userFields) # Decora o método com 'marshal_with' para formatar a resposta com os campos definidos em 'userFields'
    def post(self): # Método POST para criar um novo usuário
        args = user_args.parse_args() # Analisa os argumentos da requisição // 'args' é um dicionário com os argumentos analisados //
        
        if UserModel.query.filter_by(email=args['email']).first():
            abort(409, message="Já existe um usuário com esse email.") # Verifica se já existe um usuário com o mesmo email 
            
        user = UserModel(nome=args['nome'], email=args['email']) # Cria um novo usuário com os dados fornecidos
        db.session.add(user)
        db.session.commit() # Adiciona o novo usuário à sessão do banco de dados
        return UserModel.query.all(), 201 # Faz uma consulta no banco de dados para obter todos os usuários e retorna a lista de usuários e o código de status 201 (Criado)
    
class User(Resource): # Cria uma classe 'User' que herda de 'Resource'
    @marshal_with(userFields) # Decora o método com 'marshal_with' para formatar a resposta com os campos definidos em 'userFields'
    def get(self, id): # Método GET para obter um usuário específico
        user = UserModel.query.filter_by(id=id).first() # Faz uma consulta no banco de dados para obter o usuário com o ID fornecido
        if not user:
            abort(404, message="Usuário não encontrado.") # Se o usuário não for encontrado, retorna um erro 404
        return user # Retorna o usuário encontrado

    @marshal_with(userFields) # Decora o método com 'marshal_with' para formatar a resposta com os campos definidos em 'userFields'
    def patch(self, id): # Método PATCH para atualizar um usuário específico
        args = user_args.parse_args() # Analisa os argumentos da requisição
        user = UserModel.query.filter_by(id=id).first() # Faz uma consulta no banco de dados para obter o usuário com o ID fornecido
        if not user:
            abort(404, message="Usuário não encontrado.") # Se o usuário não for encontrado, retorna um erro 404
        user.nome = args['nome'] # Atualiza o nome do usuário
        user.email = args['email'] # Atualiza o email do usuário
        db.session.commit() # Salva as alterações no banco de dados
        return user # Retorna o usuário atualizado
    
    @marshal_with(userFields) # Decora o método com 'marshal_with' para formatar a resposta com os campos definidos em 'userFields'
    def delete(self, id): # Método DELETE para excluir um usuário específico
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="Usuário não encontrado.")
        db.session.delete(user)
        db.session.commit()
        return UserModel.query.all()