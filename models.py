# Arquivo responsável por guardar nossos modelos de Banco de Dados

from db import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_completo = db.Column(db.String(150), nullable = False)
    cpf= db.Column(db.String(150), nullable = False, unique = True)
    email= db.Column(db.String(320), nullable = False, unique = True)
    telefone = db.Column(db.String(20), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    numero_casa = db.Column(db.String(15), nullable=False)
    data_inicial = db.Column(db.DateTime, nullable=False)
    dia_vencimento = db.Column(db.Integer, nullable=False)
                         
    mensalidades = db.relationship(
        'Mensalidade',
        backref='cliente',
        lazy=True,
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<{self.nome_completo}>"

class Mensalidade(db.Model):
    __tablename__ = 'mensalidades'
    id = db.Column(db.Integer, primary_key=True)
    vencimento = db.Column(db.Date)
    valor = db.Column(db.Float)
    status = db.Column(db.String(20), default="Pendente")
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))