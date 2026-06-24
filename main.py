from flask import Flask, render_template, redirect, url_for, request, flash, session
from email_validator import validate_email, EmailNotValidError
from app.database import create_db, login_user, new_user, user_data, id_from_email
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")

# Verifica se o email é verdadeiro
def check_email(email):
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError:
        return False
    return True

# Rota original
@app.route('/')
def template():
    return redirect(url_for('login'))

# Rota Home
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', nome=session['nome'], id=session['user_id'])

# Rota Logout
@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.clear()
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['POST','GET'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        pw = request.form.get('password')

        # Verifica de email é verdadeiro
        if not check_email(email):
            flash('Email ou Senha incorretos')
            return redirect(url_for('login'))
        
        result = login_user(email, pw)

        if result == 'Check':
            # Login
            data = user_data(id_from_email(email)[0])
            session['user_id'] = data[0]
            nn = data[1].split()
            session['nome'] = nn[0]

            return redirect(url_for('home'))
        else:
            # Retorna uma mensagem de erro
            flash(result)
            return redirect(url_for('login'))

    return render_template('login.html')

# Cadastro
@app.route('/cadastro', methods=['GET','POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('nome')
        password = request.form.get('password')
        email = request.form.get('email')
        estado = request.form.get('estado')

        # Senha inválida
        if not password or len(password) < 8:
            flash("A senha precisa ter pelo menos 8 caracteres")
            return redirect(url_for("register"))

        # Email inválido
        if not check_email(email):
            flash('O email inserido não é válido. Tente novamente com um email válido')
            return redirect(url_for('register'))
        
        result = new_user(name,password,email,estado)
        if not result:
            flash('O email inserido ja está cadastrado. Tente novamente com outro email')
            return redirect(url_for('register'))
    
        flash("Conta criada com sucesso! Faça login para continuar.")
        return redirect(url_for("login"))
    
    return render_template('newuser.html')

# Termos
@app.route('/termos')
def termos():
    return 'Termos. <a href="/cadastro">Voltar</a>'

# Executar app
if __name__ == '__main__':
    create_db()
    app.run(debug=True)
