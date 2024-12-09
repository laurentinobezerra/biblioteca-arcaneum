# 📚 Biblioteca Arcaneum - Sistema CRUD com Flask, PostgreSQL e Python

---

## 📖 **Descrição do Projeto**

O projeto **Biblioteca Arcaneum** é uma aplicação web com funcionalidades CRUD (Create, Read, Update, Delete) para gerenciar dados relacionados a categorias, livros, leitores, empréstimos e um ranking de leitores mais ativos. Desenvolvido com **Flask** como framework web e **PostgreSQL** como banco de dados, a aplicação permite gerenciar informações da biblioteca com uma interface amigável baseada em HTML.

---

## ⚙️ **Tecnologias Usadas**

- **Python**: Linguagem principal no desenvolvimento da lógica do sistema.
- **Flask**: Framework web usado para estruturar o sistema de rotas e interações.
  - *Como funciona?*: Flask é um microframework leve que possibilita criar rotas, renderizar templates HTML e tratar requisições HTTP.
- **PostgreSQL 17.2**: Sistema de banco de dados relacional utilizado para armazenar as informações de empréstimos, livros, leitores, categorias e suas interações.
- **BrModelo e pgAdmin4**: Ferramentas usadas para modelagem de dados e administração do banco PostgreSQL.

---

## 📂 **Estrutura do Projeto**
```bash
biblioteca-arcaneum/
│
├── app.py                        # Configuração principal do Flask e inicialização do banco
│
├── models.py                     # Definições das tabelas e ORM com SQLAlchemy
|
│
├── routes/                        
│   ├── categorias.py             # Lógica relacionada a categorias
│   ├── livros.py                 # Lógica relacionada a livros
│   ├── leitores.py               # Lógica relacionada a leitores
│   └── emprestimos.py            # Lógica relacionada a empréstimos
│
├── templates/                    # Templates HTML usados para renderizar as páginas
│   ├── index.html
│   ├── categorias.html
│   ├── livros.html
│   ├── editar_livro.html
│   ├── leitores.html
│   ├── editar_leitor.html
│   ├── emprestimos.html
│   ├── editar_emprestimo.html
│   └── ranking_leitores.html
│
├── .env                           # Variáveis seguras, como URI do banco de dados
│
├── requirements.txt              # Lista de pacotes necessários para o ambiente
│
└── README.md                     # Documentação do projeto


```
---

## 🛠️ **Configuração e Execução**

### 📦 **Passos para Instalação**

1. Clone o repositório:
   ```bash
   git clone https://github.com/biblioteca-arcaneum.git
   cd biblioteca-arcaneum
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure o banco PostgreSQL
    - Certifique-se de que o PostgreSQL 17.2 está instalado.
    - Ajuste o arquivo `.env` com a URI de conexão correta para o banco     de dados:
    ```bash
    DATABASE_URI=postgresql+psycopg2://usuario:senha@localhost:5432/biblioteca
    ```

---
## 🚀 **Execução do Projeto**
Após a instalação e configuração:
```bash
python app.py
```
O servidor será iniciado em `http:localhost:5153`. Acesse com o navegador e comece a interagir com o sistema

---
## 📜 **Pré-requisitos**
- Banco de Dados **PostgreSQL** instalado.
- Python 3.x instalado