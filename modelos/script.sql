CREATE DATABASE biblioteca
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE categorias(
	id_categoria SERIAL PRIMARY KEY,
	nome_categoria VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE livros(
	id_livro SERIAL PRIMARY KEY,
	titulo VARCHAR(255) NOT NULL,
	id_categoria INTEGER NOT NULL,
	autor VARCHAR(255) NOT NULL,
	editora VARCHAR(255),
	ano_publicacao INTEGER,
	FOREIGN KEY(id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE leitores(
	id_leitor SERIAL PRIMARY KEY,
	cpf CHAR(11) NOT NULL UNIQUE,
	nome VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	telefone CHAR(11)
);

CREATE TABLE emprestimos(
	id_emprestimo SERIAL PRIMARY KEY,
	id_leitor INTEGER NOT NULL,
	id_livro INTEGER NOT NULL,
	data_emprestimo DATE NOT NULL,
	data_devolucao DATE,
	status VARCHAR(20) NOT NULL,
	FOREIGN KEY(id_leitor) REFERENCES leitores(id_leitor),
	FOREIGN KEY(id_livro) REFERENCES livros(id_livro)
);