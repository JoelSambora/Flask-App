import os
import pymysql
from flask_mysqldb import MySQL
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
import mysql.connector
import mysql.connector as mysql
import re
import urllib.request
urllib.request.urlopen("http://www.python.org")
# create a flask instance
app = Flask(__name__)

# add database
connection = mysql.connect(host='localhost',
                                database='teste',
                                user='root',
                                password='')

#initialize the databese

mysql = MySQL(app)
mysql.init_app(app)
# Secret key!
app.config['SECRET_KEY'] = 'Thisissuposedtobesecret!'

bootstrap = Bootstrap(app)

#index /  pagina inicial
@app.route('/login/index')
def index():
    
    if 'loggedin' in session:
        return render_template("includes/index.html")
    else:
        return redirect(url_for('login'))
       # return render_template("includes/index.html")


#função about/ sobre nos
@app.route('/about')
def about():
    return render_template("includes/about.html")

#login
@app.route('/login', methods=['GET','POST'])
def login():
    
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    #check if email and password post requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        
        email = request.form['email']
        senha = request.form['senha']
        
        #check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE Email = %s AND Senha = %s', (email, senha))
        
        users = cursor.fetchone()
        
        #if account exists in users tabale in out database
        if users:
            session['loggedin'] = True
            session['Id'] = users[0]
            session['email'] =  users[1]
           
            return redirect(url_for('index'))
        else:
            flash('Email/senha incorrecta', 'danger')
            
    return render_template("accounts/login.html")

#dashbord page
@app.route('/login/dashbord')
def dashbord():
    
    if 'loggedin' in session:
        
        return render_template("includes/dashbord.html", user_email=session['email'])
        
    return redirect(url_for('login'))   
    # last = cursor.lastrowid
  
#logout rout
@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    
    return redirect(url_for('login'))

#colaboradores
@app.route('/users/<nome_user>')
def user(nome_user):
    return render_template("users.html",nome_user=nome_user)    

#create colaborador
@app.route('/register', methods=['GET','POST'])
def create():
    name = None
 
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        
        if request.method == "POST":
            print('passou passou')

            nome = request.form['nome']
            email = request.form['email']
            genero = request.form['genero']
            provinvia = request.form['provincia']
            avenida = request.form['avenida']
            bairro= request.form['bairro']
            nrCasa = request.form['casaNumero']
            telefone = request.form['telefone'] 
            senha = request.form['password']
            confirme_senha = request.form['confirmarsenha']
            
            cursor.execute('SELECT * FROM Users WHERE email = %s', (email))
            account =  cursor.fetchone()
            
            print('cheguei')
            
            if account:
                flash('Já existe uma conta', 'danger')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Email invalido', 'danger')
            elif not re.match(r'/[A-zÁ-ú]*$', nome):
                flash('Nome invalido', 'danger')
            elif not re.match(r'/[A-zÁ-ú]*$', avenida):
                flash('Avenida invalido', 'danger')
            elif not re.match(r'/[A-zÁ-ú]*$', bairro):
                flash('Bairro invalido', 'danger')
            elif not senha is confirme_senha:
                flash('Senhas não são iguais', 'danger')
            else:
                
                #table users        
                cursor.execute(''' INSERT INTO Users VALUES(%s,%s,%s)''',(email,'',senha))
                mysql.connection.commit()
                cursor.close()
                
                #id last user
                cursor.execute("SELECT * from Users")
                record = cursor.fetchall()
                last_id = record[-1][0] 
                
                # table colaboradores
                cursor = connection.cursor()
                            
                cursor.execute(''' INSERT INTO Colaboradores VALUES(%s,%s,%s)''',(last_id,nome,genero))
                mysql.connection.commit()
                cursor.close()
                
                # table endereco
                cursor = connection.cursor()
                
                cursor.execute(''' INSERT INTO Endereco VALUES(%s,%s,%s,%s,%s)''',(last_id,provinvia,avenida,bairro,nrCasa))
                mysql.connection.commit()
                cursor.close()
                
                # table telefone
                cursor = connection.cursor()
                
                cursor.execute(''' INSERT INTO Telefone VALUES(%s,%s)''',(last_id,telefone))
                mysql.connection.commit()
                cursor.close()
                
                mysql.connection.commit()
                cursor.close()
                flash('Usuário criado com sucesso', 'success')

            return redirect(url_for('includes/dashbord.html'))
        elif request.method == 'POST':
            flash('Preencha o formulário!', 'danger')
            
    return render_template("accounts/register.html")

# função que retorna erro para página que não existe
@app.route('/<string:nome>')
def error(nome):
    variavel = f'Página ({nome}) não existe!'
    return render_template("includes/error.html", variavel2=variavel)
    
if __name__ == "__main__":
    app.run(debug=True)
