print('Iniciando Servidor Flask...') #

from flask import Flask # Serve para criar o servidor
from flask_sqlalchemy import SQLAlchemy # ORM (Mapa Objeto-Relacional) para interagir com o Banco de Dados usando objetos do Python

app = Flask(__name__) #Flask é uma classe que representa a aplicação web. // '__name__' é uma variável especial de scripts python.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Define a URL de conexão com o banco de dados // 'sqlite:///database.db' quer dizer que o banco será salvo como um arquivo local chamado 'database.db'
db = SQLAlchemy(app) # 

class UserModel(db.Model): # define uma tabela chamda 'user_model' no banco. Herda de 'db.Model', que transforma a classe num modelo de banco de dados.
    id = db.Column(db.Integer, primary_key=True) # define a colna "id" como tipo inteiro, com chave primária
    name = db.Column(db.String(80), unique=True, nullable=False) # define a coluna 'name' como tipo string, com no máximo 80 caracteres // 'unique=True': não pode haver 2 usuários iguais // 'nullable=False': não pode ser nulo
    email = db.Column(db.String(80), unique=True, nullable=False) # define a coluna 'email' como tipo string, com no máximo 80 caracteres
    
    def __repr__(self): # Método especial que define como o objeto será impresso (útil para debug e logs).
         return f"User(name = {self.name}, email = {self.email})"

@app.route('/') # define a rota '/' (ou seja, a página principal)
def home(): #homepage // Quanto o navegador acessar 'localhost:5000/', essa fundão será chamada
        return '<h1>Flask REST API </h1>' #retorna HTML simples
    
if __name__ == '__main__': #Garante que o servidor Flask só será executado se este arquivo for o princpal (e não importado por outro)
    app.run(debug=True) # ativa o modo de desenvolvimento: atualização automática ao salvar & exibe erros detalhados no navegador.
