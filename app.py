import os
import pymysql
from flask_mysqldb import MySQL
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
import mysql.connector
import mysql.connector as mysql
import re
import urllib.request
import hashlib
from datetime import timedelta


# with urllib.request.urlopen("http://www.python.org") as response:
#    html = response.read()
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

# timeout session
#@app.before_request
#def make_session_permanent():
   # session.permanent = True
   # app.permanent_session_lifetime = timedelta(minutes=5)
    
#index /  pagina inicial
@app.route('/login/index')
def index():
    
    if 'loggedin' in session:
        return render_template("includes/index.html")
    else:
        return redirect(url_for('login'))
       # return render_template("includes/index.html")


#função about/ sobre nos
@app.route('/login/about')
def about():
    if 'loggedin' in session:
        return render_template("includes/index.html")
    else:
        return redirect(url_for('login'))

#login
@app.route('/login', methods=['GET','POST'])
def login():
    
    cursor = connection.cursor(buffered=True)
    
    #check if email and password post requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        
        email = request.form['email']
        senha = request.form['senha']
        h = hashlib.md5(senha.encode()).hexdigest()

        #check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE Email = %s AND Senha = %s', (email, h))
        
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

#dashboard page
@app.route('/login/dashboard')
def dashboard():
    cursor = connection.cursor(buffered=True)
    if 'loggedin' in session:
        
        cursor.execute('SELECT * FROM users INNER JOIN colaboradores ON users.Id = colaboradores.Users_id')
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['Nome'] = user[6]
        return render_template("includes/dashboard.html", user_email=session['Nome'])
        
    return redirect(url_for('login'))   
    # last = cursor.lastrowid
  
#logout rout
@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    
    return redirect(url_for('login'))

#home route
@app.route('/')
def home():
    if 'loggedin' in session:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM colaboradores INNER JOIN users ON users.Id = colaboradores.Users_id')
        user = cursor.fetchall()
        return render_template("includes/users.html", record=user)
    else:
        return redirect(url_for('login')) 
    
#colaboradores
@app.route('/login/users/')
def users():
    
    if 'loggedin' in session:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM colaboradores INNER JOIN users ON users.Id = colaboradores.Users_id INNER JOIN telefone ON Colaboradores_ID = colaboradores.id  ORDER BY colaboradores.id')
        user = cursor.fetchall()
        return render_template("includes/users.html", record=user)
    else:
        return redirect(url_for('login'))  

#create colaborador
@app.route('/login/register', methods=['GET','POST'])
def register():
    if 'loggedin' in session:
        
        if request.method == "POST" and 'Nome' in request.form and 'Email' in request.form and 'Avenida' in request.form and 'Bairro' in request.form and 'CasaNumero' in request.form and 'phone' in request.form and 'Senha' in request.form:
            print('passou passou')

            nome = request.form['Nome']
            email = request.form['Email']
            genero = request.form['Genero']
            provincia = request.form['Provincia']
            avenida = request.form['Avenida']
            bairro= request.form['Bairro']
            nrCasa = request.form.get('CasaNumero')
            telefone = request.form.get('phone') 
            senha = request.form.get('Senha')
            h = hashlib.md5(senha.encode()).hexdigest()
            cursor = connection.cursor(buffered=True)
            
            cursor.execute('SELECT * FROM Users WHERE email = %s', (email,))
            account =  cursor.fetchone()
                        
            if account:
                flash('Já existe uma conta', 'danger')
                return redirect(url_for('register'))
            
            else:
                
                #table users        
                cursor.execute(''' INSERT INTO users (email, is_Admin, senha) VALUES(%s,%s,%s)''',(email,0,h))
                connection.commit()
                cursor.close()
                
                #id last user
                cursor = connection.cursor(buffered=True)
                cursor.execute("SELECT * from users")
                record = cursor.fetchall()
                last_id = record[-1][0] 
                
                # table colaboradores
                cursor = connection.cursor(buffered=True)
                            
                cursor.execute(''' INSERT INTO colaboradores (Users_id, Nome, Genero) VALUES(%s,%s,%s)''',(last_id,nome,genero))
                connection.commit()
                cursor.close()
                
                # table endereco
                cursor = connection.cursor(buffered=True)
                
                cursor.execute("SELECT * from colaboradores")
                record = cursor.fetchall()
                last_id = record[-1][0] 
                print(last_id)
                
                cursor.execute(''' INSERT INTO endereco (Colaboradores_ID, Provincia, Avenida, Bairro, Casa_Numero) VALUES(%s,%s,%s,%s,%s)''',(last_id,provincia,avenida,bairro,nrCasa))
                connection.commit()
                cursor.close()
                
                # table telefone
                cursor = connection.cursor(buffered=True)
                
                cursor.execute(''' INSERT INTO telefone (Colaboradores_ID, Telefone) VALUES(%s,%s)''',(last_id,telefone))
                connection.commit()
                cursor.close()
                
                flash('Usuário criado com sucesso', 'success')

                return redirect(url_for('dashboard'))
        elif request.method == 'POST':
            flash('Preencha o formulário!', 'danger')
    else:  
        return redirect(url_for('login'))
               
    return render_template("accounts/register.html")

#edit colaborador
@app.route('/edit/<int:id>')
def edit(id):
    if 'loggedin' in session:
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM colaboradores INNER JOIN users ON users.Id = colaboradores.Users_id INNER JOIN telefone ON Colaboradores_ID = colaboradores.id INNER JOIN endereco ON endereco.Colaboradores_ID = colaboradores.id Where colaboradores.id = %s', (id,))
        #cursor.execute('SELECT * FROM colaboradores Where colaboradores.id = %s', (id,))
        account =  cursor.fetchone()              

        if account:
            return render_template("accounts/edit.html", record=account)
        else:
            flash('Não existe nenhum colaborador com esse identificador', 'danger')
            redirect(url_for('users'))
            cursor.close()
 
    redirect(url_for('users'))

#update colaborador
@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    if 'loggedin' in session:
        cursor = connection.cursor(buffered=True)

        cursor.execute('SELECT * FROM colaboradores Where colaboradores.id = %s', (id,))

        account =  cursor.fetchone()
        print(account)        
        if account:
            
            if request.method == "POST" and 'Nome' in request.form and 'Email' in request.form and 'Avenida' in request.form and 'Bairro' in request.form and 'CasaNumero' in request.form and 'phone' in request.form and 'Senha' in request.form:

                nome = request.form.get('Nome')
                print(nome)
                email = request.form['Email']
                genero = request.form['Genero']
                provincia = request.form['Provincia']
                avenida = request.form['Avenida']
                print(avenida)
                bairro= request.form['Bairro']
                print(bairro)
                nrCasa = request.form.get('CasaNumero')
                telefone = request.form.get('phone') 
                senha = request.form.get('Senha')
                h = hashlib.md5(senha.encode()).hexdigest()               
                if account:
                    
                    #table users        
                    cursor.execute(" UPDATE users SET email=%s, is_Admin=%s, senha=%s WHERE id =%s;",(email,0,h,account[1],))
                    connection.commit()
                    cursor.close()
                    
                    # table colaboradores
                    cursor = connection.cursor(buffered=True)
                                
                    cursor.execute(" UPDATE colaboradores SET Nome=%s, Genero=%s WHERE id=%s; ",(nome, genero, id,))
                    print(nome)

                    connection.commit()
                    cursor.close()
                    
                    # table endereco
                    cursor = connection.cursor(buffered=True)
                                       
                    cursor.execute(" UPDATE endereco SET Provincia=%s, Avenida=%s, Bairro=%s, Casa_Numero=%s WHERE Colaboradores_ID = %s; ",( provincia, avenida, bairro, nrCasa, id,))
                    connection.commit()
                    cursor.close()
                    
                    # table telefone
                    cursor = connection.cursor(buffered=True)
                    
                    cursor.execute(" UPDATE telefone SET Telefone = %s WHERE Colaboradores_ID = %s;",(telefone, id,))
                    connection.commit()
                    cursor.close()
                    
                    flash('Colaborador atualizado com sucesso', 'success')

                    return redirect(url_for('dashboard'))
            elif request.method == 'POST':
                flash('Preencha o formulário!', 'danger')
        
        else:
            flash('Não existe uma conta com esse identificador', 'danger')
            return redirect(url_for('users'))
    cursor = connection.cursor(buffered=True)
    print('passou')
    cursor.execute('SELECT * FROM colaboradores Where colaboradores.id = %s', (id,))
    account =  cursor.fetchone()              

    print(account)
    return redirect(url_for('login'))

#delete colaborador
@app.route('/delete/<int:id>')
def delete(id):
    if 'loggedin' in session:
        
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM colaboradores Where colaboradores.id = %s', (id,))
        account =  cursor.fetchone()
        
        if account:
            
            cursor.execute('DELETE * FROM colaboradores INNER JOIN users ON users.Id = colaboradores.Users_id INNER JOIN telefone ON Colaboradores_ID = colaboradores.id INNER JOIN endereco ON endereco.Colaboradores_ID = colaboradores.id Where colaboradores.id = %s', (id,))
        else:
            flash('Não existe uma conta com esse identificador', 'danger')
            return redirect(url_for('users'))
        
    else:
        flash('Não esta logado', 'danger')
        return redirect(url_for('users')) 

# função que retorna erro para página que não existe
@app.route('/<string:nome>')
def error(nome):
    variavel = f'Página ({nome}) não existe!'
    return render_template("includes/error.html", variavel2=variavel)
    
if __name__ == "__main__":
    app.run(debug=True)