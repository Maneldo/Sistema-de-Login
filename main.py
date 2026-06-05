from flask import Flask, render_template, redirect, url_for, request
from app import database
app = Flask(__name__)

@app.route('/')
def template():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST','GET'])
def login():
    return render_template('login.html')

@app.route('/cadastro')
def register():
    return render_template('newuser.html')

if __name__ == '__main__':
    app.run(debug=True)
