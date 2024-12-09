from flask import Blueprint, render_template, request, redirect  # Importando as funções necessárias do Flask
from models import db, Categoria, Livro  # Importando a instância db e as classes do banco de dados

# Criando o blueprint para gerenciar rotas relacionadas às categorias
categorias_bp = Blueprint('categorias', __name__, url_prefix="/categorias")


# Rota principal para listar todas as categorias
@categorias_bp.route('/')
def categorias():
    # Recuperar todas as categorias do banco de dados, ordenando pelo nome
    categorias = Categoria.query.order_by(Categoria.nome_categoria).all()
    # Renderizar a página com as categorias no template
    return render_template("categorias.html", categorias=categorias)


# Rota para criar uma nova categoria
@categorias_bp.route('/create', methods=['POST'])
def criar_categoria():
    # Obter o nome da nova categoria a partir do formulário
    nome_categoria = request.form['nome_categoria']
    # Verificar se a categoria já existe no banco de dados
    categoria_existente = Categoria.query.filter_by(nome_categoria=nome_categoria).first()
    if categoria_existente:
        # Caso exista, retornar à tela com mensagem informando o erro
        categorias = Categoria.query.order_by(Categoria.nome_categoria).all()
        return render_template("categorias.html", categorias=categorias, mensagem="Essa categoria já existe!")

    # Caso contrário, criar a nova categoria e salvar no banco de dados
    nova_categoria = Categoria(nome_categoria=nome_categoria)
    db.session.add(nova_categoria)
    db.session.commit()
    # Redirecionar de volta para a página de categorias
    return redirect('/categorias')


# Rota para excluir uma categoria
@categorias_bp.route('/delete/<int:id_categoria>', methods=["POST"])
def excluir_categoria(id_categoria):
    # Verificar se a categoria possui livros associados
    livros_dependentes = Livro.query.filter(Livro.id_categoria == id_categoria).first()

    if livros_dependentes:
        # Caso existam livros associados, retornar mensagem informando o erro
        categorias = Categoria.query.order_by(Categoria.nome_categoria).all()
        return render_template("categorias.html", categorias=categorias,
                               mensagem2="Não é possível excluir esta categoria porque existem livros associados a ela!")

    # Caso contrário, buscar a categoria e removê-la do banco de dados
    categoria = Categoria.query.get(id_categoria)
    if categoria:
        db.session.delete(categoria)
        db.session.commit()

    # Redirecionar de volta para a página de categorias
    return redirect('/categorias')


# Rota para atualizar uma categoria
@categorias_bp.route('/update/<int:id_categoria>', methods=['POST'])
def alterar_categoria(id_categoria):
    # Recuperar a categoria do banco de dados
    categoria = Categoria.query.get(id_categoria)

    if categoria:
        # Atualizar o nome da categoria a partir do formulário
        categoria.nome_categoria = request.form['nome_categoria']
        db.session.commit()
    
    # Redirecionar de volta para a página de categorias
    return redirect('/categorias')
