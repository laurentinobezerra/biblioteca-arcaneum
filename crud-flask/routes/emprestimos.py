from flask import Blueprint, render_template, request, redirect  # Importando as funções necessárias do Flask
from datetime import date  # Importando funções de data
from models import db, Emprestimo, Livro, Leitor  # Importando as classes e instância db do banco
from collections import Counter  # Importando Counter para contagem de estatísticas


# Criando o blueprint para rotas relacionadas aos empréstimos
emprestimos_bp = Blueprint("emprestimos", __name__, url_prefix='/emprestimos')

# Estrutura para armazenar estatísticas de empréstimos
estatisticas = Counter()


# Função para atualizar as estatísticas de empréstimos no Counter
def atualizar_estatisticas(emprestimo, acao="adicionar"):
    if acao == "adicionar":
        estatisticas[emprestimo.id_leitor] += 1
    elif acao == "remover" and estatisticas[emprestimo.id_leitor] > 0:
        estatisticas[emprestimo.id_leitor] -= 1


# Rota principal para listar todos os empréstimos, livros e leitores
@emprestimos_bp.route('/')
def emprestimos():
    # Recuperando todos os empréstimos, livros e leitores do banco de dados
    emprestimos = Emprestimo.query.order_by(Emprestimo.status).all()
    livros = Livro.query.order_by(Livro.titulo).all()
    leitores = Leitor.query.order_by(Leitor.nome).all()
    # Renderizando a página com empréstimos, livros e leitores
    return render_template("emprestimos.html", emprestimos=emprestimos, livros=livros, leitores=leitores)


# Rota para criar um novo empréstimo
@emprestimos_bp.route('/create', methods=['POST'])
def criar_emprestimo():
    # Criando um novo objeto Emprestimo com dados do formulário
    novo_emprestimo = Emprestimo(
        id_leitor=request.form['id_leitor'],
        id_livro=request.form['id_livro'],
        data_emprestimo=date.fromisoformat(request.form['data_emprestimo']),
        status="ativo"
    )

    # Verificar se o livro já está emprestado
    livro_emprestado = Emprestimo.query.filter(
        Emprestimo.id_livro == novo_emprestimo.id_livro,
        Emprestimo.status.in_(['ativo', 'pendente'])
    ).first()

    # Verificar se o leitor já está com empréstimos pendentes ou ativos
    leitor_pendente = Emprestimo.query.filter(
        Emprestimo.id_leitor == novo_emprestimo.id_leitor,
        Emprestimo.status.in_(['ativo', 'pendente'])
    ).first()

    if livro_emprestado:
        # Caso o livro já esteja emprestado, retornar mensagem para o usuário
        return render_template("emprestimos.html",
                               emprestimos=Emprestimo.query.all(),
                               livros=Livro.query.all(),
                               leitores=Leitor.query.all(),
                               mensagem=f"O livro selecionado possui um empréstimo {livro_emprestado.status}!")

    if leitor_pendente:
        # Caso o leitor já tenha empréstimo pendente, retornar mensagem para o usuário
        return render_template("emprestimos.html",
                               emprestimos=Emprestimo.query.all(),
                               livros=Livro.query.all(),
                               leitores=Leitor.query.all(),
                               mensagem=f"O leitor selecionado possui um empréstimo {leitor_pendente.status}!")

    # Caso contrário, salvar o novo empréstimo no banco
    novo_emprestimo.status = novo_emprestimo.verificar_status()
    db.session.add(novo_emprestimo)
    db.session.commit()
    # Atualizar estatísticas
    atualizar_estatisticas(novo_emprestimo, acao="adicionar")
    return redirect('/emprestimos')


# Rota para editar dados de um empréstimo
@emprestimos_bp.route('/edit/<int:id_emprestimo>', methods=['GET'])
def editar_emprestimo(id_emprestimo):
    # Recuperar dados do empréstimo e listas de livros e leitores
    emprestimo = Emprestimo.query.get(id_emprestimo)
    livros = Livro.query.order_by(Livro.titulo).all()
    leitores = Leitor.query.order_by(Leitor.nome).all()
    # Renderizando a página de edição com dados necessários
    return render_template("editar_emprestimo.html", emprestimo=emprestimo, livros=livros, leitores=leitores)


# Rota para atualizar os dados de um empréstimo
@emprestimos_bp.route('/update/<int:id_emprestimo>', methods=['POST'])
def atualizar_emprestimo(id_emprestimo):
    emprestimo = Emprestimo.query.get(id_emprestimo)

    # Atualizar os dados de empréstimo com base no formulário
    emprestimo.data_emprestimo = date.fromisoformat(request.form['data_emprestimo'])
    emprestimo.data_devolucao = date.fromisoformat(request.form['data_devolucao']) if request.form['data_devolucao'] else None
    emprestimo.id_livro = request.form['id_livro']
    emprestimo.id_leitor = request.form['id_leitor']

    # Verificar conflitos
    livro_emprestado = Emprestimo.query.filter(
        Emprestimo.id_livro == emprestimo.id_livro,
        Emprestimo.status.in_(['ativo', 'pendente']),
        Emprestimo.id_emprestimo != id_emprestimo
    ).first()

    leitor_pendente = Emprestimo.query.filter(
        Emprestimo.id_leitor == emprestimo.id_leitor,
        Emprestimo.status.in_(['ativo', 'pendente']),
        Emprestimo.id_emprestimo != id_emprestimo
    ).first()

    if livro_emprestado or leitor_pendente:
        # Caso haja conflito, retornar mensagem para o usuário
        return render_template("editar_emprestimo.html",
                               emprestimo=emprestimo,
                               livros=Livro.query.all(),
                               leitores=Leitor.query.all(),
                               mensagem="Conflito detectado com o livro ou leitor selecionado!")

    emprestimo.status = emprestimo.verificar_status()
    db.session.commit()
    return redirect('/emprestimos')


# Rota para deletar um empréstimo
@emprestimos_bp.route('/delete/<int:id_emprestimo>', methods=['POST'])
def excluir_emprestimo(id_emprestimo):
    emprestimo = Emprestimo.query.get(id_emprestimo)
    if emprestimo:
        atualizar_estatisticas(emprestimo, acao="remover")
        db.session.delete(emprestimo)
        db.session.commit()
    return redirect('/emprestimos')


# Página para estatísticas com dados da estrutura Counter
@emprestimos_bp.route('/ranking_leitores')
def ranking_leitores():
    global estatisticas
    estatisticas = Counter()
    for emprestimo in Emprestimo.query.all():
        estatisticas[emprestimo.id_leitor] += 1
    id_leitores = {leitor.id_leitor: leitor.nome for leitor in Leitor.query.all()}
    dados_mapeados = {id_leitores.get(k, "Desconhecido"): v for k, v in estatisticas.items()}
    return render_template("ranking_leitores.html", leitores_ativos=dados_mapeados)