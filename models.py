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
    
    def __repr__(self):
        return f"<{self.nome_completo}>"