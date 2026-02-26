# Skylink

Sistema web para **controle e gerenciamento de clientes de provedor de internet**, desenvolvido com Python e Flask, utilizando SQLite como banco de dados.

Repositório: [https://github.com/flavinharv/Skylink](https://github.com/flavinharv/Skylink)

---

## Sobre o Projeto

O **Skylink** é um sistema web desenvolvido para auxiliar no gerenciamento de clientes, permitindo cadastro, edição, exclusão e controle de informações de forma organizada e prática.

O sistema utiliza arquitetura baseada em Flask, com separação entre:

* Backend (Python + Flask)
* Banco de Dados (SQLite + SQLAlchemy)
* Frontend (HTML, CSS e JavaScript)

---

## Tecnologias Utilizadas

* Python 
* Flask
* SQLAlchemy
* SQLite
* HTML5
* CSS3
* JavaScript
* Bootstrap

---

## Estrutura do Projeto

```
Skylink/
│
├── app.py              # Arquivo principal da aplicação
├── main.py             # Inicialização do sistema
├── db.py               # Configuração do banco de dados
├── models.py           # Modelos das tabelas
│
├── templates/          # Arquivos HTML
├── static/             # CSS, JS e arquivos estáticos
├── instance/           # Banco de dados SQLite
└── venv/               # Ambiente virtual
```

---

## Como Instalar o Projeto

### Clonar o repositório

```bash
git clone https://github.com/flavinharv/Skylink.git
cd Skylink
```

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar o ambiente virtual

 Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Instalar as dependências

Se houver `requirements.txt`:

```bash
pip install -r requirements.txt
```

Se não houver, instale manualmente:

```bash
pip install flask flask_sqlalchemy
```

---

## Como Executar

Com o ambiente virtual ativado:

```bash
python app.py
```

ou

```bash
python main.py
```

Depois acesse no navegador:

```
http://127.0.0.1:5000
```

---

## Banco de Dados

O sistema utiliza **SQLite**, que cria automaticamente o arquivo `.db` dentro da pasta `instance/`.

As tabelas são criadas com base nos modelos definidos em `models.py`.

---

## Funcionalidades

* Cadastro de clientes
* Edição de dados
* Exclusão de clientes
* Listagem de registros
* Integração com banco de dados
* Interface web interativa

---

## Desenvolvedores

Projeto desenvolvido por **Flávia Rhavena M. C. de Almeida, Maria Rita Xavier Lopes e Sabrina Dourado da Silva** 💙

---

## Licença

Este projeto é para fins acadêmicos e de aprendizado.
