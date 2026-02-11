from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.schemas import BookCreate, BookResponse

app = FastAPI(title="Bible API", version="1.0.0")

# Configuração de templates
templates = Jinja2Templates(directory="app/templates")


# Rota para exibir a página
@app.get("/admin/books", response_class=HTMLResponse)
def admin_books_page(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse(
        "books.html",
        {"request": request, "books": books},
    )


# Rota para criar um livro via formulário
@app.post("/admin/books/create")
def create_book_form(
    name: str = Form(...), abbreviation: str = Form(...), db: Session = Depends(get_db)
):
    # Cria o livro
    new_book = Book(name=name, abbreviation=abbreviation)
    db.add(new_book)
    db.commit()

    # Redireciona de volta para a página
    return RedirectResponse(url="/admin/books", status_code=303)


# Rota para deletar livro (API)
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # Busca o livro
    book = db.query(Book).filter(Book.id == book_id).first()

    # Se não encotrar retorna 404
    if not book:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Deleta o livro
    db.delete(book)
    db.commit()

    return None  # 204 não retorna conteúdo


# Rota para deletar via formulário (interface web)
@app.post("/admin/books/delete/{book_id}")
def delete_book_form(book_id: int, db: Session = Depends(get_db)):
    # Busca o livro
    book = db.query(Book).filter(Book.id == book_id).first()

    if book:
        db.delete(book)
        db.commit()

    # Redireciona de volta para a página
    return RedirectResponse(url="/admin/books", status_code=303)


# Rota para exibir formulário de edição
@app.get("/admin/books/edit/{book_id}", response_class=HTMLResponse)
def edit_book_page(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    return templates.TemplateResponse(
        "edit_book.html", {"request": request, "book": book}
    )


# Rota para processar edição via formulário
@app.post("/admin/books/update/{book_id}")
def update_book_form(
    book_id: int,
    name: str = Form(...),
    abbreviation: str = Form(...),
    db: Session = Depends(get_db),
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    book.name = name
    book.abbreviation = abbreviation
    db.commit()

    return RedirectResponse(url="/admin/books", status_code=303)


# Rota para atualizar o livro (API)
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    # Busca o livro
    db_book = db.query(Book).filter(Book.id == book_id).first()

    # Se não encontrar, retorna 404
    if not db_book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Atualiza os campos
    db_book.name = book.name
    db_book.abbreviation = book.abbreviation

    # Salva no banco
    db.commit()
    db.refresh(db_book)

    return db_book


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(name=book.name, abbreviation=book.abbreviation)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
