from email import message
import os
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


app = Flask(__name__)

class RegisterForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired(), Length(min=4, max=24)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Email invalido'), Length(max=50)])
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max=15), ], render_kw={"placeholder": "test"})

class LoginForm(FlaskForm):
    email = StringField('',validators=[InputRequired(), Email(message='Email invalido'), Length(max=50)])
    password = PasswordField('', validators=[InputRequired(), Length(min=8, max=15)])
#index /  pagina inicial
@app.route('/')
def index():
    return render_template("includes/index.html")

#função about/ sobre nos
@app.route('/about')
def about():
    return render_template("includes/about.html")

#login
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template("accounts/login.html", form=form)

#colaboradores
@app.route('/users/<nome_user>')
def user(nome_user):
    return render_template("users.html",nome_user=nome_user)    

#create colaborador
@app.route('/register', methods=['GET','POST'])
def create():
    form = RegisterForm()
    
    return render_template("accounts/register.html", form = form)

# função que retorna erro para página que não existe
@app.route('/<string:nome>')
def error(nome):
    variavel = f'Página ({nome}) não existe!'
    return render_template("includes/error.html", variavel2=variavel)

bootstrap = Bootstrap(app)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
    
if __name__ == "__main__":
    app.run(debug=True)
