def test_list_chapter_by_book(client, db_session):
    # 1. Arrange - Cria um livro com capítulos
    from app.models.book import Book
    from app.models.chapter import Chapter

    book = Book(name="João", abbreviation="Jo")
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    chapter1 = Chapter(number=1, book_id=book.id)
    chapter2 = Chapter(number=2, book_id=book.id)
    chapter3 = Chapter(number=3, book_id=book.id)

    db_session.add_all([chapter1, chapter2, chapter3])
    db_session.commit()

    # 2. Act - Busca capítulos do livro
    response = client.get(f"/books/{book.id}/chapters")

    # 3. Assert - Verifica a resposta
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["number"] == 1
    assert data[1]["number"] == 2
    assert data[2]["number"] == 3
    assert all(ch["book_id"] == book.id for ch in data)
