from flask import Flask, request, redirect, url_for, render_template_string, session

app = Flask(__name__)
app.secret_key = 'secret'  # Necessário para usar sessões no Flask

# Banco de dados simulado (usuários e senhas)
users = {
    "user1": {"password": "password1", "role": "admin", "data": "Informações confidenciais do admin."},
    "user2": {"password": "password2", "role": "user", "data": "Informações privadas do usuário."},
    "user3": {"password": "password3", "role": "user", "data": "Informações de outro usuário."}
}

# Função de autenticação simulada
def check_user(username, password):
    user = users.get(username)
    if user and user['password'] == password:
        return user
    return None

# Página principal
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('perfil', username=session['username']))
    return redirect(url_for('login'))

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_user(username, password)
        if user:
            session['username'] = username  # Armazenando o nome de usuário na sessão
            return redirect(url_for('perfil', username=username))
        else:
            return "Credenciais inválidas", 403

    return render_template_string("""
        <h2>Login</h2>
        <form method="POST">
            Nome de usuário: <input type="text" name="username"><br>
            Senha: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    """)

# Página de perfil do usuário (vulnerabilidade Broken Access Control aqui)
@app.route('/perfil/<username>')
def perfil(username):
    # **Vulnerabilidade:** qualquer usuário pode acessar o perfil de outro usuário manipulando a URL
    user = users.get(username)
    if not user:
        return "Usuário não encontrado", 404
    
    return f"Bem-vindo ao perfil de {username}! {user['data']}"

if __name__ == '__main__':
    app.run(debug=True)
