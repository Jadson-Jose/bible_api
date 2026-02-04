from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.schemas import BookCreate, BookResponse

app = FastAPI(title="Bible API", version="1.0.0")


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(name=book.name, abbreviation=book.abbreviation)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book
