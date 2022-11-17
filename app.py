import os
from flask_mysqldb import MySQL
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
import mysql.connector
import mysql.connector as mysql
from flask_wtf.csrf import CSRFProtect
import hashlib
from datetime import datetime

# add database
connection = mysql.connect(host='localhost',
                                         database='teste',
                                         user='root',
                                         password='')

app = Flask(__name__)

#initialize the databese
db = MySQL(app)

mysql = MySQL(app)

# Secret key!
app.config['SECRET_KEY'] = 'Thisissuposedtobesecret!'

bootstrap = Bootstrap(app)


# timeout session
#@app.before_request
#def make_session_permanent():
   # session.permanent = True
   # app.permanent_session_lifetime = timedelta(minutes=5)
userId = None
csrf = CSRFProtect()

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
    
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:

        cursor = connection.cursor(buffered=True)
    
    #check if email and password post requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form:
        
        email = request.form['email']
        senha = request.form['senha']
        h = hashlib.md5(senha.encode()).hexdigest()

        #check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE Email = %s AND Senha = %s', (email, h))
        users = cursor.fetchone()
        global userId 
        userId = users[0]    
        #if account exists in users tabale in out database
        if users:
            session['loggedin'] = True
            session['Id'] = users[0]
            session['email'] =  users[1]
            session['is_Admin'] = users[2]

            is_Admin = session['is_Admin']
            
            # returns current date and time
            now = datetime.now()
            
            #insert into table date_time                
            cursor.execute(''' INSERT INTO date_time (d_data, tipo, Colaboradores_ID) VALUES(%s,%s,%s)''',(now,1,findIDcolaborador(userId),))
            print(userId)
            connection.commit()
            cursor.close()
            
            if is_Admin != 0:
                return render_template("includes/index.html", is_Admin = is_Admin)
            else:
                return redirect(url_for('index'))
        else:
            flash('Email/senha incorrecta', 'danger')
            
    return render_template("accounts/login.html")

#find id colaborador

def findIDcolaborador(id):
    cursor = connection.cursor(buffered=True)
    cursor.execute('SELECT colaboradores.id FROM colaboradores INNER JOIN users ON users.Id =%s AND users.Id = colaboradores.Users_id', (id,))
    user = cursor.fetchone()
    return user[0]


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
            session['is_Admin'] = user[2]
            is_Admin = session['is_Admin']
            
            if is_Admin != 0:
                return render_template("includes/dashboard.html", user_email=session['Nome'])
            else:
                return render_template("includes/index.html")
    flash('precisa fazer login para aceder a página','info')  
    return redirect(url_for('login'))   
    # last = cursor.lastrowid

#logout rout
@app.route('/login/logout')
    
def logout():
    cursor = connection.cursor(buffered=True)
    if 'loggedin' in session:
        
        userId = session['Id']
        now = datetime.now()
                
        # insert into table date_time                
        cursor.execute(''' INSERT INTO date_time (d_data, tipo, Colaboradores_ID) VALUES(%s,%s,%s)''',(now,0,findIDcolaborador(userId),))
        connection.commit()
        cursor.close()
        
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('email', None)
        
        return redirect(url_for('login'))
    else:
        flash('precisa fazer login para aceder a página','info')
        return redirect(url_for('login'))


#colaboradores
@app.route('/')

def home():
    
    if 'loggedin' in session:
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM colaboradores INNER JOIN users ON users.Id = colaboradores.Users_id')
        user = cursor.fetchall()
        return render_template("includes/users.html", record=user)
    else:
        flash('precisa fazer login para aceder a página','info')
        return redirect(url_for('login')) 
    
# lista dos colaboradores 
@app.route('/login/users/')

def users():
    
    if 'loggedin' in session:
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM colaboradores INNER JOIN users ON users.Id = colaboradores.Users_id INNER JOIN telefone ON Colaboradores_ID = colaboradores.id  ORDER BY colaboradores.id')
        user = cursor.fetchall()
        return render_template("includes/users.html", record=user)
    else:
        flash('precisa fazer login para aceder a página','info')
        return redirect(url_for('login'))  

# lista de presensa
@app.route('/login/presensa')
def presensa():
    if 'loggedin' in session:
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT colaboradores.id, colaboradores.nome, date_time.d_data, date_time.tipo  FROM colaboradores INNER JOIN date_time ON date_time.Colaboradores_ID = colaboradores.id  ORDER BY colaboradores.id')
        user = cursor.fetchall()
        print(user)
        return render_template("includes/presensa.html", record=user)
    else:
        flash('precisa fazer login para aceder a página','info')
        return redirect(url_for('login')) 

#create colaborador
@app.route('/login/register', methods=['GET','POST'])

def register():
    if 'loggedin' in session:
        
        if request.method == "POST" and 'Nome' in request.form and 'Email' in request.form and 'Avenida' in request.form and 'Bairro' in request.form and 'CasaNumero' in request.form and 'phone' in request.form and 'Senha' in request.form:

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
        flash('precisa fazer login para aceder a página','info')
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
    else:
        flash('precisa fazer login para aceder a página','info')
        return redirect(url_for('login'))

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
        
    flash('precisa fazer login para aceder a página','info')
    return redirect(url_for('login'))

#delete colaborador
@app.route('/delete/<int:id>')

def delete(id):
    if 'loggedin' in session:
        cursor = connection.cursor(buffered=True)
        cursor.execute('SELECT * FROM colaboradores Where colaboradores.id = %s', (id,))
        account =  cursor.fetchone()
        
        user_id = None
        
        if account:
            #DELETE FROM COLABORADORES WHERE ID = ?
            cursor.execute('SELECT Users_id FROM colaboradores WHERE Id = %s', (id,))
            x = cursor.fetchone()
            user_id = x[0]
           
            cursor.execute('DELETE FROM telefone WHERE Colaboradores_ID = %s',(id,))            
            connection.commit()
            
            cursor.execute('DELETE FROM endereco WHERE Colaboradores_ID = %s',(id,))            
            connection.commit()
            
            cursor.execute('DELETE FROM colaboradores WHERE id = %s',(id,))            
            connection.commit()
            
            cursor.execute('DELETE FROM users WHERE Id = %s',(user_id,))            
            connection.commit()

            cursor.close()
            
            flash('Conta apagada com sucesso', 'success')
            return redirect(url_for('users'))
        else:
            flash('Não existe uma conta com esse identificador', 'danger')
            return redirect(url_for('users'))
        
    flash('precisa fazer login para aceder a página','info')
    return redirect(url_for('login'))

# função que retorna erro para página que não existe
@app.route('/<string:nome>')
def error(nome):
    variavel = f'Página ({nome}) não existe!'
    return render_template("includes/error.html", variavel2=variavel)
    
if __name__ == "__main__":
    app.run(debug=True)
    csrf.init_app(app)
