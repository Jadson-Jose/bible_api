def test_create_chapter(client, db_session):
    # 1. Arrange - Cria um livro primeiro
    from app.models.book import Book

    book = Book(
        name="Gênesis",
        abbreviation="Gn",
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    book_id = book.id

    # 2. Act - Cria um capítulo para esse livro
    chapter_data = {
        "number": 1,
        "book_id": book_id,
    }
    response = client.post("/chapters", json=chapter_data)

    # 3. Assert - verifica se foi criado
    assert response.status_code == 201
    data = response.json()
    assert data["number"] == 1
    assert data["book_id"] == book_id
    assert "id" in data
