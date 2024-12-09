from flask import Blueprint, render_template, request, redirect  # Importando funções necessárias do Flask
from models import db, Categoria, Livro  # Importando a instância do banco de dados e as classes necessárias

# Criando o blueprint para as rotas de livros
livros_bp = Blueprint('livros', __name__, url_prefix="/livros")


# Rota base para listar todos os livros e suas categorias
@livros_bp.route('/')
def livros():
    # Recuperando todos os livros e categorias do banco
    livros = Livro.query.all()
    categorias = Categoria.query.order_by(Categoria.nome_categoria).all()
    # Renderizando a lista no template
    return render_template("livros.html", livros=livros, categorias=categorias)


# Rota para criar um novo livro no banco
@livros_bp.route('/create', methods=['POST'])
def criar_livro():
    # Criando um novo objeto Livro com dados do formulário
    novo_livro = Livro(
        titulo=request.form['titulo'],
        id_categoria=request.form['id_categoria'],
        autor=request.form['autor'],
        editora=request.form['editora'],
        ano_publicacao=request.form['ano_publicacao']
    )
    # Salvando o livro no banco de dados
    db.session.add(novo_livro)
    db.session.commit()
    return redirect('/livros')


# Rota para excluir um livro específico
@livros_bp.route('/delete/<int:id_livro>', methods=['POST'])
def excluir_livro(id_livro):
    livro = Livro.query.get(id_livro)
    if livro:
        db.session.delete(livro)
        db.session.commit()
    return redirect('/livros')


# Rota para exibir a tela de edição de um livro específico
@livros_bp.route('/edit/<int:id_livro>', methods=['GET'])
def editar_livro(id_livro):
    livro = Livro.query.get(id_livro)
    categorias = Categoria.query.order_by(Categoria.nome_categoria).all()
    return render_template('editar_livro.html', livro=livro, categorias=categorias)


# Rota para atualizar os dados de um livro no banco de dados
@livros_bp.route('/update/<int:id_livro>', methods=['POST'])
def atualizar_livro(id_livro):
    livro = Livro.query.get(id_livro)
    if livro:
        livro.titulo = request.form['titulo']
        livro.id_categoria = request.form['id_categoria']
        livro.autor = request.form['autor']
        livro.editora = request.form['editora']
        livro.ano_publicacao = request.form['ano_publicacao']
        db.session.commit()
    return redirect('/livros')