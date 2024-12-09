from flask_sqlalchemy import SQLAlchemy  # Importando a instância SQLAlchemy para o gerenciamento do banco de dados
from datetime import date, timedelta  # Importando classes para manipulação de datas

# Criando uma instância do SQLAlchemy
db = SQLAlchemy()


# Classe para representar a tabela de Categorias no banco de dados
class Categoria(db.Model):
    __tablename__ = "categorias"  # Nome da tabela no banco de dados
    id_categoria = db.Column(db.Integer, primary_key=True)  # Chave primária da tabela
    nome_categoria = db.Column(db.String(100), unique=True, nullable=False)  # Nome da categoria, único e obrigatório


# Classe para representar a tabela de Livros no banco de dados
class Livro(db.Model):
    __tablename__ = "livros"  # Nome da tabela no banco de dados
    id_livro = db.Column(db.Integer, primary_key=True)  # Chave primária da tabela
    titulo = db.Column(db.String(255), nullable=False)  # Título do livro (obrigatório)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)  # Chave estrangeira para categorias
    autor = db.Column(db.String(255), nullable=False)  # Nome do autor (obrigatório)
    editora = db.Column(db.String(255))  # Nome da editora
    ano_publicacao = db.Column(db.Integer)  # Ano de publicação do livro

    # Relacionamento entre livros e categorias
    categoria = db.relationship('Categoria', backref='livros', lazy=True)


# Classe para representar a tabela de Leitores no banco de dados
class Leitor(db.Model):
    __tablename__ = "leitores"  # Nome da tabela no banco de dados
    id_leitor = db.Column(db.Integer, primary_key=True)  # Chave primária da tabela
    cpf = db.Column(db.String(11), unique=True, nullable=False)  # CPF do leitor (único e obrigatório)
    nome = db.Column(db.String(255), nullable=False)  # Nome do leitor (obrigatório)
    email = db.Column(db.String(255), unique=True, nullable=False)  # Email do leitor (único e obrigatório)
    telefone = db.Column(db.String(11))  # Telefone do leitor


# Classe para representar a tabela de Empréstimos no banco de dados
class Emprestimo(db.Model):
    __tablename__ = "emprestimos"  # Nome da tabela no banco de dados
    id_emprestimo = db.Column(db.Integer, primary_key=True)  # Chave primária da tabela
    id_leitor = db.Column(db.Integer, db.ForeignKey('leitores.id_leitor'), nullable=False)  # Chave estrangeira para a tabela de Leitores
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.id_livro'), nullable=False)  # Chave estrangeira para a tabela de Livros
    data_emprestimo = db.Column(db.Date, nullable=False)  # Data do empréstimo
    data_devolucao = db.Column(db.Date)  # Data de devolução (pode ser nula)
    status = db.Column(db.String(20), nullable=False, default="ativo")  # Status do empréstimo, com valor padrão como "ativo"

    # Relacionamentos entre empréstimos, livros e leitores
    livro = db.relationship('Livro', backref='emprestimos')
    leitor = db.relationship('Leitor', backref='emprestimos')

    # Método para verificar o status de um empréstimo
    def verificar_status(self):
        # Tratar a data de empréstimo se ela for uma string
        if isinstance(self.data_emprestimo, str):
            data_emprestimo = date.fromisoformat(self.data_emprestimo)
        else:
            data_emprestimo = self.data_emprestimo

        hoje = date.today()  # Obter a data atual
        prazo_maximo = data_emprestimo + timedelta(days=30)  # Calcular o prazo de 30 dias

        # Lógica para determinar o status do empréstimo
        if self.data_devolucao:
            return "devolvido"  # Se houver uma data de devolução, o status é "devolvido"
        elif hoje > prazo_maximo:
            return "pendente"  # Se ultrapassou o prazo sem devolução, o status é "pendente"
        return "ativo"  # Caso contrário, o status é "ativo"