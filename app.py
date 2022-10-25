from email import message
import os
from flask import Flask, render_template, flash,redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SelectField, TelField
from wtforms.validators import InputRequired, Email, Length


app = Flask(__name__)

class RegisterForm(FlaskForm):

    nome = StringField('Nome', validators=[InputRequired(), Length(min=4, max=24)], render_kw={"placeholder": "Nome completo"})
    email = StringField('Email', validators=[InputRequired(), Email(message='Email invalido'), Length(max=50)], render_kw={"placeholder": "anavoice@ana.com"})
    provincia = SelectField(u'Província', choices=[('MC', 'Maputo Cidade'), ('MP', 'Maputo Província')])
    avenida = StringField('Avenida', validators=[InputRequired(), Length(min=4, max=24)], render_kw={"placeholder": "Avenida"})
    bairro = StringField('bairro', validators=[InputRequired(), Length(min=4, max=24)], render_kw={"placeholder": "bairro"})
    telefone = TelField('Número de telefone', [InputRequired(), Length(min=9, max=9)], render_kw={"placeholder": "840000000"})
    casaNumero = TelField('Número da casa', [InputRequired(), Length(min=1, max=9)])
    password = PasswordField('Senha', validators=[Length(min=8, max=15), ], render_kw={"placeholder": "Senha do colaborador"})

class LoginForm(FlaskForm):
    email = StringField('',validators=[InputRequired(), Email(message='Email invalido'), Length(max=50)], render_kw={"placeholder": "Seu email"})
    password = PasswordField('', validators=[InputRequired(), Length(min=8, max=15)], render_kw={"placeholder": "Sua senha"})
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
    if form.validate_on_submit():
       flash('Usuário criado com sucesso', 'success')
    
    if not form.validate_on_submit():
        flash('Usuário não registrado', 'error')
        
        #return '<h1>' + form.nome.data +' '+ form.email.data +'</h1>'
    # if request.method == 'POST':
    #     for file in request.files.getlist('file'):
    #         file.save(os.path.join(app.config['UPLOAD_DIR'], file.filename))
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
