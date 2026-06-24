import sqlite3
import bcrypt

# Criar banco de dados
def create_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL,
    password BLOB NOT NULL,
    email TEXT NOT NULL UNIQUE,
    data_criacao TEXT DEFAULT CURRENT_DATE NOT NULL,
    estado TEXT NOT NULL
)
''')
    conn.commit()
    conn.close()
    
# Verificar de email ja está cadastrado
def check_email(email):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT email FROM usuarios WHERE email=?', (email,))
    result = cur.fetchone()
    conn.close()

    return result is not None

# Criar novo usuario, se email ja está cadastro, impedir que o email seja cadastrado
def new_user(name, password, email, estado):
    # Se email existe, abortar criação
    if check_email(email):
        return False
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Criptografar senhas em hash
    scode = password.encode('utf-8')
    senha_cripto = bcrypt.hashpw(scode, bcrypt.gensalt())

    cur.execute('''
    INSERT INTO usuarios (nome, password, email, estado)
    VALUES (?,?,?,?)
    ''', (name, senha_cripto, email, estado))
    conn.commit()
    conn.close()
    
    return True

# Tentar Logar usuario, checando email inserido e senha
def login_user(email, password):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT password FROM usuarios WHERE email=?', (email,))
    # Pegar senha criptografada
    result = cur.fetchone()
    conn.close()

    if result:
        sqlpass = result[0] 
        newpass = password.encode('utf-8')
        # Conferir senhas criptografadas
        if bcrypt.checkpw(newpass, sqlpass):
            return 'Check'
    
    return 'Email ou Senha incorretos'

def id_from_email(email):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM usuarios WHERE email=?', (email,))
    # Pegar dados
    result = cur.fetchone()
    conn.close()
    return result

def user_data(id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id=?', (id,))
    # Pegar dados
    result = cur.fetchone()
    conn.close()
    return result
