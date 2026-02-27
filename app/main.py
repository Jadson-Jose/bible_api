from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.models.chapter import Chapter
from app.models.verse import Verse
from app.schemas import (
    BookCreate,
    BookResponse,
    ChapterCreate,
    ChapterResponse,
    VerseCreate,
    Verseresponse,
)

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


@app.post(
    "/chapters", status_code=status.HTTP_201_CREATED, response_model=ChapterResponse
)
def create_chapter(chapter: ChapterCreate, db: Session = Depends(get_db)):
    # Verifica se o livro existe
    book = db.query(Book).filter(Book.id == chapter.book_id).first()  # ← CORRIGIDO
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Cria o capítulo
    db_chapter = Chapter(number=chapter.number, book_id=chapter.book_id)  # ← CORRIGIDO

    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)

    return db_chapter


# Rota para exibir página de capítulos de um livro
@app.get("/admin/books/{book_id}/chapters", response_class=HTMLResponse)
def admin_chapter_page(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    chapters = (
        db.query(Chapter)
        .filter(Chapter.book_id == book_id)
        .order_by(Chapter.number)
        .all()
    )

    return templates.TemplateResponse(
        "chapters.html",
        {
            "request": request,
            "book": book,
            "chapters": chapters,
        },
    )


# Rota para criar capítulo via formulário
@app.post("/admin/books/{book_id}/chapters/create")
def create_chapter_form(
    book_id: int, number: int = Form(...), db: Session = Depends(get_db)
):
    # Verifica se o livro existe
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Cria o capítulo
    chapter = Chapter(number=number, book_id=book_id)
    db.add(chapter)
    db.commit()

    return RedirectResponse(url=f"/admin/books/{book_id}/chapters", status_code=303)


# Rota para deletar capítulo via formulário
@app.post("/admin/books/{book_id}/chapters/delete/{chapter_id}")
def delete_chapter_form(book_id: int, chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()

    if chapter:
        db.delete(chapter)
        db.commit()
    return RedirectResponse(url=f"/admin/books/{book_id}/chapters", status_code=303)


@app.post("/verses", status_code=status.HTTP_201_CREATED, response_model=Verseresponse)
def create_verse(verse: VerseCreate, db: Session = Depends(get_db)):
    # Verifica se o capítulo existe
    chapter = db.query(Chapter).filter(Chapter.id == verse.chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Capítulo não encontrado")

    # Cria o versículo
    db_verse = Verse(number=verse.number, text=verse.text, chapter_id=verse.chapter_id)

    db.add(db_verse)
    db.commit()
    db.refresh(db_verse)

    return db_verse


# Rota para exibir página de versículos de um capítulo
@app.get(
    "/admin/books/{book_id}/chapters/{chapter_id}/verses", response_class=HTMLResponse
)
def admin_verses_page(
    book_id: int, chapter_id: int, request: Request, db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()

    if not book or not chapter:
        raise HTTPException(status_code=404, detail="Livro ou capítulo não encontrado")

    verses = (
        db.query(Verse)
        .filter(Verse.chapter_id == chapter_id)
        .order_by(Verse.number)
        .all()
    )

    return templates.TemplateResponse(
        "verses.html",
        {"request": request, "book": book, "chapter": chapter, "verses": verses},
    )


# Rota para criar versiculos via formulaŕio
@app.post("/admin/books/{book_id}/chapters/{chapter_id}/verses/create")
def create_verse_form(
    book_id: int,
    chapter_id: int,
    number: int = Form(...),
    text: str = Form(...),
    db: Session = Depends(get_db),
):
    # Verifica se o capítulo existe
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()

    if not chapter:
        HTTPException(status_code=404, detail="Capíulo não encontrado")

    # Cria o versículo
    verse = Verse(number=number, text=text, chapter_id=chapter_id)
    db.add(verse)
    db.commit()

    return RedirectResponse(
        url=f"/admin/books/{book_id}/chapters/{chapter_id}/verses",
        status_code=303,
    )


# Rota para deletar versículo via formulário
@app.post("/admin/books/{book_id}/chapters/{chapters_id}/verses/delete/{verse_id}")
def delete_verse_form(
    book_id: int, chapter_id: int, verse_id: int, db: Session = Depends(get_db)
):
    verse = db.query(Verse).filter(Verse.id == verse_id).first()

    if verse:
        db.delete(verse)
        db.commit()

    return RedirectResponse(
        url=f"/admin/books/{book_id}/chapters/{chapter_id}/verses",
        status_code=303,
    )


@app.get("/books", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book


@app.get("/books/{book_id}/chapters", response_model=list[ChapterResponse])
def list_chapters(book_id: int, db: Session = Depends(get_db)):
    # Verifica se o livro existe
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    # Busca capítulos do livro
    chapters = (
        db.query(Chapter)
        .filter(Chapter.book_id == book_id)
        .order_by(Chapter.number)
        .all()
    )

    return chapters


@app.get("/chapters/{chapter_id}/verses", response_model=list[Verseresponse])
def list_verses(chapter_id: int, db: Session = Depends(get_db)):
    # Verifica se o capítulo existe
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Capítulo não encontrado")

    # Busca versículos do capítulo
    verses = (
        db.query(Verse)
        .filter(Verse.chapter_id == chapter_id)
        .order_by(Verse.number)
        .all()
    )
    return verses


@app.get("/verses", response_model=list[Verseresponse])
def search_verses(search: str, db: Session = Depends(get_db)):
    query = db.query(Verse)

    # Se tem parâmetro de busca, filtra pelo texto
    if search:
        query = query.filter(Verse.text.ilike(f"%{search}%"))

    # Ordena por capítulo e número
    verses = query.order_by(Verse.chapter_id, Verse.number).all()

    return verses
