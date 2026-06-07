from flask import Flask, render_template, redirect, url_for, request, flash
from email_validator import validate_email, EmailNotValidError
from app.database import create_db, check_email, login_user

app = Flask(__name__)

app.secret_key = 'chaveultrasecretanãoreveleparaninguem'

# Verifica se o email é verdadeiro
def verificar_email(email):
    try:
        validate_email(email, check_deliverability=True)
    except EmailNotValidError:
        return 'O email inserido é inválido'
    return 'Check'

#-Rotas-#

# Rota original
@app.route('/')
def template():
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pw = request.form.get('password')
        email_chec = verificar_email(email)
        # Verifica de email é verdadeiro
        if email_chec != 'Check':
            flash('Email ou Senha incorretos')
            return redirect(url_for('login'))
        
        result = login_user(email, pw)
        
        if result == 'Check':
            # Login
            flash('Acesso Concedido')
            return redirect(url_for('login'))
        else:
            # Retorna uma mensagem de erro
            flash(result)
            return redirect(url_for('login'))

    return render_template('login.html')

# Cadastro
@app.route('/cadastro')
def register():
    return render_template('newuser.html')

# Executar app
if __name__ == '__main__':
    create_db()
    app.run(debug=True)
