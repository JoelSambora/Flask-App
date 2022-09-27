import os
from flask import Flask, render_template


app = Flask(__name__)

#index /  pagina inicial
@app.route('/')
def index():
    return render_template("index.html")

#função about/ sobre nos
@app.route('/about')
def about():
    return render_template("about.html")


#colaboradores
@app.route('/users/<nome_user>')
def user(nome_user):
    return render_template("users.html",nome_user=nome_user)    

# função que retorna erro para página que não existe
@app.route('/<string:nome>')
def error(nome):
    variavel = f'Página ({nome}) não existe!'
    return render_template("error.html", variavel2=variavel)
    
if __name__ == "__main__":
    app.run(debug=True)
