from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Cliente, Mensalidade
from datetime import datetime
import calendar

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skylink.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Home com listagem de clientes
    @app.route('/')
    @app.route('/home')
    def home():
        busca = request.args.get('busca')
        if busca:
            clientes = Cliente.query.filter(
                Cliente.nome_completo.ilike(f"%{busca}%")
            ).all()
        else:
            clientes = Cliente.query.all()
        return render_template('index.html', clientes=clientes)

    # Detalhes do cliente e mensalidades
    @app.route('/detalhes-cliente/<int:id>')
    def detalhesCliente(id):
        cliente = Cliente.query.get_or_404(id)
        return render_template('detalhes-cliente.html', cliente=cliente)

    # Alternar status da mensalidade
    @app.route('/alternar_status/<int:id>', methods=['POST'])
    def alternar_status(id):
        mensalidade = Mensalidade.query.get_or_404(id)
        mensalidade.status = "Pago" if mensalidade.status == "Pendente" else "Pendente"
        db.session.commit()
        return redirect(request.referrer)

    # Cadastro de cliente
    @app.route('/cadastro-cliente', methods=['POST'])
    def cadastro_cliente():
        nome = request.form['nome_completo']
        cpf = request.form['cpf']
        email = request.form['email']
        telefone = request.form['telefone']
        cep = request.form['cep']
        endereco = request.form['endereco']
        numero_casa = request.form['numero_casa']

        # Garantir número do dia da fatura

        data_inicial = datetime.strptime(request.form.get("data_inicial"), "%Y-%m-%d")
        dia_vencimento = data_inicial.day

        novo_cliente = Cliente(
            nome_completo=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            cep=cep,
            endereco=endereco,
            numero_casa=numero_casa,
            data_inicial=data_inicial,
            dia_vencimento=dia_vencimento
        )
        db.session.add(novo_cliente)
        db.session.commit()

        # Gerar mensalidades automáticas (12 meses)
        for i in range(12):
            ano = data_inicial.year
            mes = data_inicial.month + i
            while mes > 12:
                mes -= 12
                ano += 1

            ultimo_dia = calendar.monthrange(ano, mes)[1]
            dia = min(dia_vencimento, ultimo_dia)
            vencimento = datetime(ano, mes, dia)

            nova_mensalidade = Mensalidade(
                vencimento=vencimento,
                valor=80.0,
                cliente_id=novo_cliente.id
            )
            db.session.add(nova_mensalidade)

        db.session.commit()

        return redirect(url_for('home'))

    # Deletar cliente
    @app.route('/deletar/<int:id>', methods=['POST'])
    def deletar(id):
        cliente = Cliente.query.get_or_404(id)
        db.session.delete(cliente)
        db.session.commit()
        return redirect(url_for('home'))

    @app.route('/suporte')
    def suporte():
        return render_template('suporte.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)