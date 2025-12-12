from flask import Flask, render_template, request, jsonify, redirect, url_for

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    @app.route('/')
    def login():
        return render_template('login.html')

    @app.route('/home')
    def home():
        return render_template('index.html')
    
    @app.route('/atualizacao')
    def atualizacao():
        return render_template('atualizacao.html')

    @app.route('/detalhes-cliente')
    def detalhesCliente():
        return render_template('detalhes-cliente.html')

    @app.route('/cadastro')
    def cadastro():


    @app.route('/recuperar-senha')
    def recuperarSenha():
        return render_template('recuperarSenha.html')

    @app.route('/api/login', methods=['POST'])
    def api_login():
        data = request.get_json(force=True) or {}
        username = data.get('username') or data.get('email') or ''
        password = data.get('password') or ''

        USERS = {
            "admin@example.com": "admin"
        }

        if username in USERS and USERS[username] == password:
            return jsonify({"sucesso": True, "mensagem": "Login realizado com sucesso!"})
        else:
            return jsonify({"sucesso": False, "mensagem": "Usuário ou senha incorretos"}), 401
        
    @app.route('/suporte')
    def suporte():
        return render_template('suporte.html')
    
    @app.route('/atualizacao')
    def atualizacao():
        return render_template('atualizacao.html')
    
    @app.route('/detalhes-cliente')
    def detalhesCliente():
        return render_template('detalhes-cliente.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)