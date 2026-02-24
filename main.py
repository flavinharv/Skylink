from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Cliente, Mensalidade
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
db.init_app(app)

#CRIANDO AS ROTAS:

# @app.route('/')
# def login():
#     return render_template('login.html')

# COLOQUEI PARA ABRIR O HOME PRIMEIRO (ESTAVA TESTANDO), DEPOIS MUDE
@app.route('/')
def home():
    busca = request.args.get('busca')

    if busca:
        clientes = Cliente.query.filter(
            Cliente.nome_completo.ilike(f"{busca}%")
        ).all()

        if not clientes:
            clientes = Cliente.query.filter(
                (Cliente.nome_completo.ilike(f"%{busca}%")) |
                (Cliente.cpf.ilike(f"%{busca}%"))
            ).all()

        if not clientes:
            clientes = Cliente.query.all()
    else:
        clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):

    # Busca o cliente pelo ID
    cliente = Cliente.query.get_or_404(id)

    # Se for POST (clicou em salvar)
    if request.method == 'POST':

        # Atualiza os campos normais
        cliente.nome_completo = request.form['nome_completo']
        cliente.cpf = request.form['cpf']
        cliente.email = request.form['email']
        cliente.telefone = request.form['telefone']
        cliente.cep = request.form['cep']
        cliente.endereco = request.form['endereco']
        cliente.numero_casa = request.form['numero_casa']
        cliente.fatura = request.form['fatura']

        # 🔥 Conversão correta da data (NÃO aceita vazio)
        cliente.data_inicial = datetime.strptime(
            request.form['data_inicial'],
            "%Y-%m-%d"
        ).date()

        # Salva no banco
        db.session.commit()

        # Redireciona para home
        return redirect(url_for('home'))

    # Se for GET (abrindo a página)
    return render_template('atualizacao.html', cliente=cliente)


@app.route('/detalhes-cliente/<int:id>', methods=['GET'])
def detalhesCliente(id):
    cliente = Cliente.query.get_or_404(id)

    return render_template('detalhes-cliente.html', cliente=cliente)

@app.route('/alternar_status/<int:id>', methods=['POST'])
def alternar_status(id):
    mensalidade = Mensalidade.query.get_or_404(id)

    if mensalidade.status == "Pendente":
        mensalidade.status = "Pago"
    else:
        mensalidade.status = "Pendente"

    db.session.commit()
    return redirect(request.referrer)

@app.route('/cadastro-cliente', methods=['GET','POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        nome_completo = request.form['nome_completo']
        cpf = request.form['cpf']
        email = request.form['email']
        telefone = request.form['telefone']
        cep = request.form['cep']
        endereco = request.form['endereco']
        numero_casa = request.form['numero_casa']
        data_inicial = datetime.strptime(request.form['data_inicial'], "%Y-%m-%d")
        
        novo_cliente = Cliente(
            nome_completo=nome_completo,
            cpf=cpf,
            email=email,
            telefone=telefone,
            cep=cep,
            endereco=endereco,
            numero_casa=numero_casa,
            data_inicial=data_inicial
        )

        db.session.add(novo_cliente)
        db.session.commit()

        return redirect(url_for('home'))
    
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/recuperar-senha')
def recuperarSenha():
    return render_template('recuperarSenha.html')

@app.route('/suporte')
def suporte():
    return render_template('suporte.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
