from flask import Flask, render_template, redirect, url_for #importar biblioteca do flask e chamar a Classe Fask e a função render template que é do Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app=Flask("hello") #nome da aplicação
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)#chama o BD e manda o APP 

class Post(db.Model): #Codigo em py que explica como criar a tabela do DB, se não falar nada ele cria a tabela com nome de Post
    __tablename__='posts' #nome a tabela para não deixar automatico, nome em minuscula e no plural 
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(70), nullable=False)
    body=db.Column(db.String(500))
    created=db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(20), nullable=False, unique=True, index=True)#index pq vamos buscar muito no banco
    email=db.Column(db.String(64), nullable=False, unique=True)
    password_hash=db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author')


db.create_all() #cria as tabelas que não tem no banco, se tiver não cria novo

@app.route("/") #raiz da aplicação 
def index():
    
    posts=Post.query.all()
    return render_template("index.html", posts=posts)

@app.route("/populate")
def populate():
    user = User(username='feulo', email="g@g.com", password_hash='a')
    post1=  Post(title="post1", body="texto do post", author=user)
    post2=  Post(title="post2", body="texto do post2", author=user)
    db.session.add(user)
    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()
    return redirect(url_for('index')) #redireciona para alguma pagina.