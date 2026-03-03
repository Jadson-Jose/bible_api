# 📖 Bible API - Sistema Completo de Gerenciamento da Bíblia Sagrada

Sistema completo com Backend REST API e Frontend React para gerenciamento e leitura da Bíblia Católica (Versão Ave Maria), desenvolvido como Trabalho de Conclusão de Curso (TCC).

## 🎯 Sobre o Projeto

Este projeto implementa um sistema completo para digitalização, armazenamento e consulta da Bíblia Sagrada Católica. Possui duas interfaces distintas: uma administrativa para gerenciamento de conteúdo e uma interface moderna para leitura pelos usuários.

## ✨ Funcionalidades

### 📚 Backend - API REST (FastAPI)

**Gerenciamento de Livros:**

- CRUD completo (Criar, Ler, Atualizar, Deletar)
- Validação de nomes únicos
- Exclusão em cascata (livros, capítulos e versículos)

**Gerenciamento de Capítulos:**

- Organização hierárquica por livro
- Numeração sequencial
- Navegação intuitiva

**Gerenciamento de Versículos:**

- Cadastro com suporte para textos longos
- Busca full-text case-insensitive
- Organização por capítulo

**Interface Administrativa:**

- Painel web completo com Bootstrap 5
- Design responsivo
- Confirmações de exclusão
- Formulários validados

### 🎨 Frontend - Interface de Leitura (React)

**Experiência do Usuário:**

- Design moderno com gradientes
- Interface responsiva
- Navegação hierárquica (Livros → Capítulos → Versículos)
- Busca em tempo real
- Grid layout adaptativo

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│         Frontend React (Port 3000)          │
│  • Interface de Leitura                     │
│  • Busca de Versículos                      │
│  • Design Moderno                           │
└──────────────────┬──────────────────────────┘
                   │ HTTP Requests (Axios)
                   ▼
┌─────────────────────────────────────────────┐
│      Backend FastAPI (Port 8000)            │
│  • API REST                                 │
│  • Painel Administrativo                    │
│  • Validações                               │
└──────────────────┬──────────────────────────┘
                   │ SQLAlchemy ORM
                   ▼
┌─────────────────────────────────────────────┐
│         PostgreSQL (Port 5432)              │
│  • books → chapters → verses                │
│  • Integridade Referencial                  │
└─────────────────────────────────────────────┘
```

## 🛠️ Tecnologias Utilizadas

### Backend

- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy 2.0** - ORM para Python
- **Alembic** - Gerenciamento de migrations
- **PostgreSQL** - Banco de dados relacional
- **Pydantic** - Validação de dados
- **Pytest** - Framework de testes (11 testes automatizados)
- **Jinja2** - Templates para interface admin
- **Bootstrap 5** - Framework CSS

### Frontend

- **React 18** - Biblioteca para interfaces
- **React Router DOM** - Roteamento
- **Axios** - Cliente HTTP
- **CSS3** - Estilização moderna (Grid, Flexbox, Gradientes)

### Ferramentas

- **Git/GitHub** - Controle de versão
- **Python 3.12** - Linguagem backend
- **Node.js/npm** - Ambiente frontend
- **pip/venv** - Gerenciamento de dependências Python

## 📋 Pré-requisitos

- Python 3.12+
- Node.js 18+ e npm
- PostgreSQL 12+
- Git

## 🚀 Instalação

### Backend (bible-api)

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/bible-api.git
cd bible-api
```

#### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Configure o banco de dados

```sql
CREATE DATABASE bible_db;
CREATE DATABASE bible_test;
```

#### 5. Configure variáveis de ambiente

Crie `.env`:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/bible_db
TEST_DATABASE_URL=postgresql://usuario:senha@localhost:5432/bible_test
```

#### 6. Execute as migrations

```bash
alembic upgrade head
```

#### 7. Inicie o servidor backend

```bash
uvicorn app.main:app --reload
```

Backend disponível em: `http://localhost:8000`

---

### Frontend (bible-frontend)

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/bible-frontend.git
cd bible-frontend
```

#### 2. Instale as dependências

```bash
npm install
```

#### 3. Inicie o servidor frontend

```bash
npm start
```

Frontend disponível em: `http://localhost:3000`

---

## 🎮 Como Usar

### Para Administradores (Digitar a Bíblia)

Acesse: `http://localhost:8000/admin/books`

1. Adicione livros da Bíblia
2. Adicione capítulos a cada livro
3. Digite os versículos de cada capítulo

### Para Usuários (Ler a Bíblia)

Acesse: `http://localhost:3000`

1. Navegue pelos livros
2. Selecione um capítulo
3. Leia os versículos
4. Use a busca para encontrar trechos específicos

## 📚 Documentação da API

### Endpoints REST

#### Livros

```http
POST   /books              # Criar livro
GET    /books              # Listar todos os livros
GET    /books/{id}         # Buscar livro por ID
PUT    /books/{id}         # Atualizar livro
DELETE /books/{id}         # Deletar livro (cascata)
GET    /books/{id}/chapters # Listar capítulos de um livro
```

#### Capítulos

```http
POST   /chapters                  # Criar capítulo
GET    /chapters/{id}/verses      # Listar versículos de um capítulo
```

#### Versículos

```http
POST   /verses                    # Criar versículo
GET    /verses                    # Listar todos os versículos
GET    /verses?search=texto       # Buscar por texto (case-insensitive)
```

### Documentação Interativa

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🗄️ Estrutura do Banco de Dados

```sql
books
├── id (PK)
├── name (UNIQUE)
└── abbreviation

chapters
├── id (PK)
├── number
└── book_id (FK → books.id, ON DELETE CASCADE)

verses
├── id (PK)
├── number
├── text (TEXT)
└── chapter_id (FK → chapters.id, ON DELETE CASCADE)
```

## 🧪 Testes Automatizados

O projeto utiliza **TDD (Test-Driven Development)** com 11 testes automatizados.

### Executar testes

```bash
# Todos os testes
pytest tests/ -v --disable-warnings

# Testes específicos
pytest tests/test_books.py -v
pytest tests/test_get_books.py -v
pytest tests/test_verses.py -v

# Com cobertura
pytest tests/ --cov=app --cov-report=term-missing
```

### Testes Implementados

✅ test_create_book_with_valid_data  
✅ test_update_book  
✅ test_delete_book  
✅ test_list_all_books  
✅ test_get_book_by_id  
✅ test_get_book_not_found  
✅ test_create_chapter  
✅ test_list_chapters_by_book  
✅ test_create_verse  
✅ test_list_verses_by_chapter  
✅ test_search_verses_by_text

**Taxa de sucesso: 100% (11/11)** 🟢

## 📁 Estrutura do Projeto

```
bible-api/                      # Backend
├── alembic/                    # Migrations
│   └── versions/
├── app/
│   ├── models/                 # SQLAlchemy Models
│   │   ├── book.py
│   │   ├── chapter.py
│   │   └── verse.py
│   ├── schemas/                # Pydantic Schemas
│   │   ├── book.py
│   │   ├── chapter.py
│   │   └── verse.py
│   ├── templates/              # Jinja2 Templates
│   │   ├── base.html
│   │   ├── books.html
│   │   ├── chapters.html
│   │   ├── verses.html
│   │   └── edit_book.html
│   ├── database.py             # DB Config
│   └── main.py                 # FastAPI App
├── tests/                      # Testes Pytest
│   ├── conftest.py
│   ├── test_books.py
│   ├── test_get_books.py
│   ├── test_chapters.py
│   ├── test_get_chapters.py
│   ├── test_verses.py
│   ├── test_get_verses.py
│   ├── test_delete_book.py
│   └── test_update_book.py
├── .env
├── requirements.txt
└── README.md

bible-frontend/                 # Frontend
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   │   ├── Home.js             # Lista de livros
│   │   ├── BookChapters.js     # Lista de capítulos
│   │   └── ChapterRead.js      # Leitura de versículos
│   ├── services/
│   │   └── api.js              # Configuração Axios
│   ├── App.js                  # Rotas React Router
│   ├── App.css                 # Estilos
│   └── index.js
├── package.json
└── README.md
```

## 🎓 Metodologia TDD

Desenvolvimento guiado por testes com ciclo:

1. **🔴 RED**: Escrever teste que falha
2. **🟢 GREEN**: Implementar código mínimo para passar
3. **🔵 REFACTOR**: Melhorar mantendo testes verdes

## 🔐 Segurança

- ✅ Validação de dados com Pydantic
- ✅ Proteção contra SQL Injection (ORM)
- ✅ CORS configurado para localhost
- ✅ Constraints de integridade referencial
- ✅ Cascade delete para evitar dados órfãos
- ✅ Sanitização de inputs

## 📊 Estatísticas do Projeto

- **Linhas de código:** 1500+
- **Arquivos:** 25+
- **Testes automatizados:** 11 (100% passando)
- **Migrations:** 6
- **Endpoints:** 11
- **Páginas frontend:** 3
- **Commits:** 15+

## 🚧 Próximas Funcionalidades (Trabalhos Futuros)

- [ ] Autenticação JWT
- [ ] Deploy (Heroku/Railway)
- [ ] Docker containerization
- [ ] CI/CD com GitHub Actions
- [ ] Paginação de resultados
- [ ] Cache de consultas
- [ ] Refatoração em módulos (routes/, services/)
- [ ] Testes E2E com Cypress

## 👨‍💻 Autor

**Jadson Silva**  
Trabalho de Conclusão de Curso  
Desenvolvimento de Sistemas

## 📄 Licença

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso acadêmico.

## 🙏 Agradecimentos

- Orientador do TCC
- Comunidade FastAPI e React
- Documentação da Bíblia Católica Ave Maria
- Stack Overflow e GitHub Community

---

## 📞 Contato

Para dúvidas ou sugestões sobre o projeto:

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- Email: seu-email@example.com

---

⭐ **Desenvolvido com dedicação para digitalização da Palavra de Deus** ⭐

🎓 **TCC 2026 - Sistema Completo de Gerenciamento Bíblico** 🎓
