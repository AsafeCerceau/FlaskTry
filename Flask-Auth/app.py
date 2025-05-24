from flask import Flask, render_template, url_for, redirect #importa a biblioteca Flask para criar a aplicação web
from flask_sqlalchemy import SQLAlchemy #importa a biblioteca SQLAlchemy para manipulação de banco de dados
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user #importa a biblioteca UserMixin para autenticação de usuários
from flask_wtf import FlaskForm #importa a biblioteca FlaskForm para criar formulários
from wtforms import StringField, PasswordField, SubmitField #importa os tipos de campos para criar formulários
from wtforms.validators import InputRequired, Length, ValidationError #importa os validadores para validar os campos do formulário
from flask_bcrypt import Bcrypt #importa a biblioteca Bcrypt para criptografar senhas

app = Flask(__name__)
bcrypt = Bcrypt(app) #Cria uma instância do Bcrypt para criptografar senhas
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #Define o banco de dados e conecta esse arquivo com a aplicação
app.config['SECRET_KEY'] = 'aquiestaachavesecreta' #Define a chave secreta para proteger o banco de dados

db = SQLAlchemy(app)

login_manager = LoginManager() #Cria uma instância do LoginManager para gerenciar o login de usuários
login_manager.init_app(app) #Inicializa o LoginManager com a aplicação Flask
login_manager.login_view = "login" #Define a rota de login para o LoginManager

@login_manager.user_loader
def load_user(user_id): #Função que carrega o usuário pelo id
    return User.query.get(int(user_id)) #Retorna o usuário do banco de dados com o id fornecido


class User(db.Model, UserMixin): #Cria a classe User que representa a tabela de usuários no banco de dados
    id = db.Column(db.Integer, primary_key=True) #Define a coluna id como chave primária
    username = db.Column(db.String(35), unique=True, nullable=False) #Define a coluna username como string única e não nula
    password = db.Column(db.String(80), nullable=False) #Define a coluna password como string não nula
    
class RegisterForm(FlaskForm): #Cria a classe RegisterForm que representa o formulário de registro
    username = StringField(validators=[InputRequired(), Length( #Define o campo username como string com tamanho mínimo e máximo
        min=4, max=35)], render_kw = {'placeholder': 'Username'}) #placeholder é o texto que aparece no campo antes de o usuário digitar algo
    
    password = PasswordField (validators=[InputRequired(), Length( # Define o campo password como string com tamanho mínimo e máximo       
        min=4, max=80)], render_kw = {'placeholder': 'Password'}) 
    
    submit = SubmitField('Register') #Define o botão de submit como 'Register'
    
    def validade_usarname(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first() #Verifica se o username já existe no banco de dados
        if existing_user_username:
            raise ValidationError(
                'Esse usuário já existe. Escolha outro.') #Se o username já existe, levanta um erro de validação


class LoginForm(FlaskForm): #Cria a classe RegisterForm que representa o formulário de registro
    username = StringField(validators=[InputRequired(), Length( #Define o campo username como string com tamanho mínimo e máximo
        min=4, max=35)], render_kw = {'placeholder': 'Username'}) #placeholder é o texto que aparece no campo antes de o usuário digitar algo
    
    password = PasswordField (validators=[InputRequired(), Length( # Define o campo password como string com tamanho mínimo e máximo       
        min=4, max=80)], render_kw = {'placeholder': 'Password'}) 
    
    submit = SubmitField('Login') #Define o botão de submit como 'Login'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST']) #Define a rota para o login)
def login():
    form = LoginForm()
    if form.validate_on_submit(): # Quando o usuário tentar fazer login
        user = User.query.filter_by(username=form.username.data).first() # Busca o usuário no banco de dados pelo username
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data): #se a senha fornecida pelo usuário for igual à senha criptografada no banco de dados
                login_user(user) #faz o login do usuário
                return redirect(url_for('dashboard')) # Após o login bem-sucedido, o usuário será redirecionado para a página do dashboard
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST']) #Define a rota para o dashboard
@login_required
def dashboard():
    return render_template('dashboard.html') #A página do dashboard é onde o usuário será redirecionado após o login bem-sucedido

@app.route('/logout', methods=['GET', 'POST']) #Define a rota para o logout
@login_required
def logout():
    logout_user() #Faz o logout do usuário
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST']) #Define a rota para o registro
def register():
    form = RegisterForm()
    
    if form.validate_on_submit(): # Quando um usuário for registrado
        hashed_password = bcrypt.generate_password_hash(form.password.data) # Sua senha será criptografada
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login')) # Após o registro, o usuário será redirecionado para a página de login
    
    
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True) #Atualiza o servidor quando há mudanças no código