from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from db import db
from models import Cliente, Mensalidade
from datetime import datetime
import calendar
import pdfkit

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.secret_key = "chave_super_secreta"  # necessário para session
db.init_app(app)

# ===================== LOGIN =====================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        # Login fixo do admin
        if email == "admin@gmail.com" and senha == "admin":
            session['user'] = email
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('home'))
        else:
            flash("Email ou senha incorretos!", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Você saiu da conta.", "info")
    return redirect(url_for('login'))

# ===================== HOME =====================
@app.route('/')
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))  # protege a home

    busca = request.args.get('busca')
    if busca:
        clientes = Cliente.query.filter(
            Cliente.nome_completo.ilike(f"%{busca}%")
        ).all()
    else:
        clientes = Cliente.query.all()

    return render_template('index.html', clientes=clientes)

# ===================== CLIENTE =====================
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nome_completo = request.form['nome_completo']
        cliente.cpf = request.form['cpf']
        cliente.email = request.form['email']
        cliente.telefone = request.form['telefone']
        cliente.cep = request.form['cep']
        cliente.endereco = request.form['endereco']
        cliente.numero_casa = request.form['numero_casa']
        cliente.dia_vencimento = request.form['dia_vencimento']
        cliente.data_inicial = datetime.strptime(request.form['data_inicial'], "%Y-%m-%d").date()

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('atualizacao.html', cliente=cliente)

@app.route('/detalhes-cliente/<int:id>')
def detalhesCliente(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    cliente = Cliente.query.get_or_404(id)
    return render_template('detalhes-cliente.html', cliente=cliente)

@app.route('/gerar-pdf/<int:id>')
def gerar_pdf(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    cliente = Cliente.query.get_or_404(id)
    total_pago = sum(
        (m.valor or 0) for m in cliente.mensalidades 
        if m.status and m.status.strip().lower() == "pago"
    )
    total_pendente = sum(
        (m.valor or 0) for m in cliente.mensalidades
        if not m.status or m.status.strip().lower() != "pago"
    )

    html = render_template(
        'detalhes-cliente-pdf.html',
        cliente=cliente,
        total_pago=total_pago,
        total_pendente=total_pendente
    )

    caminho_wkhtml = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=caminho_wkhtml)

    options = {
        "page-size": "A4",
        "encoding": "UTF-8",
        "margin-top": "10mm",
        "margin-right": "10mm",
        "margin-bottom": "10mm",
        "margin-left": "10mm"
    }

    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=cliente_{cliente.id}.pdf'
    return response

@app.route('/alternar_status/<int:id>', methods=['POST'])
def alternar_status(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    mensalidade = Mensalidade.query.get_or_404(id)
    mensalidade.status = "Pago" if mensalidade.status == "Pendente" else "Pendente"
    db.session.commit()
    return redirect(request.referrer)

@app.route('/cadastro-cliente', methods=['POST'])
def cadastro():
    if 'user' not in session:
        return redirect(url_for('login'))

    nome = request.form['nome_completo']
    cpf = request.form['cpf']
    email = request.form['email']
    telefone = request.form['telefone']
    cep = request.form['cep']
    endereco = request.form['endereco']
    numero_casa = request.form['numero_casa']
    data_inicial = datetime.strptime(request.form.get("data_inicial"), "%Y-%m-%d")
    dia_vencimento = data_inicial.day

    if Cliente.query.filter_by(email=email).first():
        return "Este email já está cadastrado!", 400

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

    for i in range(12):
        ano = data_inicial.year
        mes = data_inicial.month + i
        while mes > 12:
            mes -= 12
            ano += 1
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        dia = min(dia_vencimento, ultimo_dia)
        vencimento = datetime(ano, mes, dia)
        nova_mensalidade = Mensalidade(vencimento=vencimento, valor=80.0, cliente_id=novo_cliente.id)
        db.session.add(nova_mensalidade)

    db.session.commit()
    return redirect(url_for('home'))

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    if 'user' not in session:
        return redirect(url_for('login'))

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

# ===================== RODAR APP =====================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)