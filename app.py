from flask import Flask, render_template, redirect, url_for, request, flash #importar biblioteca do flask e chamar a Classe Fask e a função render template que é do Flask, request pega o metodo da requisição
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user
from werkzeug.security import check_password_hash,generate_password_hash
from sqlalchemy.exc import IntegrityError

app=Flask("hello") #nome da aplicação
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]="pudim"

db = SQLAlchemy(app)#chama o BD e manda o APP 
login = LoginManager(app) #ajuda a criar o login


class Post(db.Model): #Codigo em py que explica como criar a tabela do DB, se não falar nada ele cria a tabela com nome de Post
    __tablename__='posts' #nome a tabela para não deixar automatico, nome em minuscula e no plural 
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(70), nullable=False)
    body=db.Column(db.String(500))
    created=db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(UserMixin, db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(20), nullable=False, unique=True, index=True)#index pq vamos buscar muito no banco
    email=db.Column(db.String(64), nullable=False, unique=True)
    password_hash=db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author')

    def set_password(self, password):
        self.password_has=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_has, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


db.create_all() #cria as tabelas que não tem no banco, se tiver não cria novo

@app.route("/") #raiz da aplicação 
def index():    
    posts=Post.query.all()
    return render_template("index.html", posts=posts)

@app.route('/register', methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method== "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:  
            flash("username or e-mail already exists!") 
        else:    
            return redirect(url_for('login'))


    return render_template('register.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Incorrect Username or Password")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))