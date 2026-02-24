# 📖 Bible API - Sistema de Gerenciamento da Bíblia Sagrada

API RESTful completa para gerenciamento e consulta da Bíblia Católica (Versão Ave Maria), desenvolvida como Trabalho de Conclusão de Curso (TCC).

## 🎯 Sobre o Projeto

Este projeto implementa uma API robusta e uma interface administrativa para digitalização, armazenamento e consulta da Bíblia Sagrada Católica. O sistema permite o cadastro completo da hierarquia bíblica (Livros → Capítulos → Versículos) e fornece endpoints para consulta e busca de conteúdo.

## ✨ Funcionalidades

### 📚 Gerenciamento de Livros

- Criar, editar, excluir e listar livros da Bíblia
- Validação de nomes únicos
- Armazenamento de abreviações

### 📑 Gerenciamento de Capítulos

- Organização de capítulos por livro
- Numeração sequencial
- Navegação hierárquica

### 📝 Gerenciamento de Versículos

- Cadastro completo de versículos
- Suporte para textos longos
- Organização por capítulo
- Interface otimizada para digitação

### 🎨 Interface Administrativa

- Painel web completo para gerenciamento
- Design responsivo com Bootstrap 5
- Navegação intuitiva entre hierarquias
- Confirmações antes de exclusões

## 🛠️ Tecnologias Utilizadas

### Backend

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM para Python
- **Alembic** - Gerenciamento de migrations
- **PostgreSQL** - Banco de dados relacional
- **Pydantic** - Validação de dados
- **Pytest** - Framework de testes

### Frontend

- **Jinja2** - Motor de templates
- **Bootstrap 5** - Framework CSS
- **HTML5/CSS3** - Estrutura e estilo

### Ferramentas

- **Git/GitHub** - Controle de versão
- **Python 3.12** - Linguagem de programação
- **pip/venv** - Gerenciamento de dependências

## 📋 Pré-requisitos

- Python 3.12+
- PostgreSQL 12+
- pip
- virtualenv (opcional, mas recomendado)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/bible-api.git
cd bible-api
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie os bancos no PostgreSQL:

```sql
CREATE DATABASE bible_db;
CREATE DATABASE bible_test;
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/bible_db
TEST_DATABASE_URL=postgresql://usuario:senha@localhost:5432/bible_test
```

### 6. Execute as migrations

```bash
alembic upgrade head
```

### 7. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## 📚 Documentação da API

### Endpoints Principais

#### Livros (Books)

```http
POST   /books              # Criar livro
PUT    /books/{id}         # Atualizar livro
DELETE /books/{id}         # Deletar livro
```

#### Capítulos (Chapters)

```http
POST   /chapters           # Criar capítulo
```

#### Versículos (Verses)

```http
POST   /verses             # Criar versículo
```

### Interface Administrativa

```http
GET /admin/books                                    # Lista de livros
GET /admin/books/{book_id}/chapters                 # Capítulos de um livro
GET /admin/books/{book_id}/chapters/{chapter_id}/verses  # Versículos de um capítulo
```

**Documentação interativa:** `http://localhost:8000/docs`

## 🗄️ Estrutura do Banco de Dados

```
books
├── id (PK)
├── name (UNIQUE)
└── abbreviation

chapters
├── id (PK)
├── number
└── book_id (FK → books.id)

verses
├── id (PK)
├── number
├── text (TEXT)
└── chapter_id (FK → chapters.id)
```

## 🧪 Testes

O projeto utiliza **TDD (Test-Driven Development)** com cobertura de testes automatizados.

### Executar todos os testes

```bash
pytest tests/ -v
```

### Executar testes específicos

```bash
pytest tests/test_books.py -v
pytest tests/test_chapters.py -v
pytest tests/test_verses.py -v
```

### Cobertura de testes

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## 📁 Estrutura do Projeto

```
bible-api/
├── alembic/                 # Migrations do banco
│   └── versions/
├── app/
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── book.py
│   │   ├── chapter.py
│   │   └── verse.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── book.py
│   │   ├── chapter.py
│   │   └── verse.py
│   ├── templates/           # Templates Jinja2
│   │   ├── base.html
│   │   ├── books.html
│   │   ├── chapters.html
│   │   ├── verses.html
│   │   └── edit_book.html
│   ├── database.py          # Configuração do banco
│   └── main.py              # Aplicação FastAPI
├── tests/                   # Testes automatizados
│   ├── conftest.py
│   ├── test_books.py
│   ├── test_chapters.py
│   ├── test_delete_book.py
│   ├── test_update_book.py
│   └── test_verses.py
├── .env                     # Variáveis de ambiente
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## 🎓 Metodologia

### Test-Driven Development (TDD)

O projeto foi desenvolvido seguindo rigorosamente a metodologia TDD:

1. **🔴 RED**: Escrever teste que falha
2. **🟢 GREEN**: Implementar código mínimo para passar
3. **🔵 REFACTOR**: Melhorar o código mantendo os testes passando

### Padrões Utilizados

- **Repository Pattern**: Separação de lógica de negócio e acesso a dados
- **RESTful API**: Endpoints seguindo convenções REST
- **MVC adaptado**: Models, Views (Templates), Controllers (Routes)

## 🔐 Segurança

- Validação de dados com Pydantic
- Proteção contra SQL Injection (SQLAlchemy ORM)
- Sanitização de inputs
- Constraints de integridade referencial no banco

## 🚧 Próximas Funcionalidades

- [ ] Endpoints GET para listagem e busca
- [ ] Sistema de busca por texto em versículos
- [ ] Paginação de resultados
- [ ] Autenticação e autorização
- [ ] API de busca avançada
- [ ] Cache de consultas frequentes
- [ ] Frontend moderno (Vue.js/React)

## 👨‍💻 Autor

**Jadson Silva**  
Trabalho de Conclusão de Curso  
[GitHub](https://github.com/seu-usuario)

## 📄 Licença

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso.

## 🙏 Agradecimentos

- Orientador do TCC
- Comunidade FastAPI
- Documentação da Bíblia Ave Maria

---

⭐ **Desenvolvido com dedicação para digitalização da Palavra de Deus** ⭐
