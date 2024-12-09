from flask import Blueprint, render_template, request, redirect  # Importando funções necessárias do Flask
from models import db, Leitor  # Importando a instância do banco de dados e a classe Leitor

# Criando blueprint para a área de leitores
leitores_bp = Blueprint("leitores", __name__, url_prefix="/leitores")


# Rota base para listar todos os leitores
@leitores_bp.route('/')
def listar_leitores():
    leitores = Leitor.query.order_by(Leitor.nome).all()
    return render_template('leitores.html', leitores=leitores)


# Rota para criar novo leitor
@leitores_bp.route('/create', methods=["POST"])
def criar_leitor():
    novo_leitor = Leitor(
        nome=request.form["nome"],
        cpf=request.form["cpf"],
        email=request.form["email"],
        telefone=request.form["telefone"]
    )

    # Validando CPF duplicado
    if Leitor.query.filter_by(cpf=novo_leitor.cpf).first():
        return render_template("leitores.html", leitores=Leitor.query.order_by(Leitor.nome).all(),
                               mensagem="CPF já cadastrado!")

    # Validando email duplicado
    if Leitor.query.filter_by(email=novo_leitor.email).first():
        return render_template("leitores.html", leitores=Leitor.query.order_by(Leitor.nome).all(),
                               mensagem="Email já cadastrado!")

    db.session.add(novo_leitor)
    db.session.commit()
    return redirect("/leitores")


# Carregar tela para edição
@leitores_bp.route('/edit/<int:id_leitor>', methods=["GET"])
def editar_leitor(id_leitor):
    leitor = Leitor.query.get(id_leitor)
    if leitor:
        return render_template("editar_leitor.html", leitor=leitor)
    return redirect('/leitores')


# Atualizar dados do leitor
@leitores_bp.route('/update/<int:id_leitor>', methods=["POST"])
def atualizar_leitor(id_leitor):
    leitor = Leitor.query.get(id_leitor)

    if leitor:
        leitor.nome = request.form["nome"]
        leitor.cpf = request.form["cpf"]
        leitor.email = request.form["email"]
        leitor.telefone = request.form["telefone"]

        db.session.commit()
    return redirect('/leitores')


# Excluir um leitor
@leitores_bp.route('/delete/<int:id_leitor>', methods=["POST"])
def excluir_leitor(id_leitor):
    leitor = Leitor.query.get(id_leitor)
    if leitor:
        db.session.delete(leitor)
        db.session.commit()
    return redirect("/leitores")
