from flask import Flask, render_template  # Importando as funções necessárias do Flask
from models import db  # Importando a instância do banco de dados SQLAlchemy
from routes.categorias import categorias_bp  # Importando o Blueprint de Categorias
from routes.livros import livros_bp  # Importando o Blueprint de Livros
from routes.leitores import leitores_bp  # Importando o Blueprint de Leitores
from routes.emprestimos import emprestimos_bp  # Importando o Blueprint de Empréstimos
import os  # Importando para trabalhar com variáveis de ambiente
from dotenv import load_dotenv  # Carregando variáveis de ambiente seguras

# Carregar as variáveis de ambiente a partir do arquivo `.env`
load_dotenv()

# Configurar o aplicativo Flask
app = Flask(__name__)  # Criando a instância da aplicação Flask
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")  # Configurando a URI do banco de dados via variável de ambiente
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativando o recurso de monitoramento de modificações do SQLAlchemy para melhorar o desempenho

# Inicializar o SQLAlchemy com a aplicação Flask
db.init_app(app)  # Associando a instância do banco de dados com a aplicação Flask

# Criar todas as tabelas no banco de dados caso ainda não existam
with app.app_context():
    db.create_all()  # Criação automática das tabelas no banco de dados

# Registrar os blueprints (rotas) no Flask
app.register_blueprint(categorias_bp)  # Registrando as rotas de categorias
app.register_blueprint(livros_bp)  # Registrando as rotas de livros
app.register_blueprint(leitores_bp)  # Registrando as rotas de leitores
app.register_blueprint(emprestimos_bp)  # Registrando as rotas de empréstimos

# Definição da rota principal (home page)
@app.route('/')
def index():
    # Renderiza a página principal
    return render_template("index.html")

# Execução da aplicação Flask
if __name__ == "__main__":
    app.run(debug=True, port=5153)  # Inicia a aplicação no modo debug na porta 5153
