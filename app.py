from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
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
    return render_template('cadastro.html')

@app.route('/senha')
def senha():
    return render_template('senha.html')

@app.route('/suporte')
def suporte():
    return render_template('suporte.html')

if __name__ == '__main__':
    app.run(debug=True)