def test_create_verse(client, db_session):
    # 1. Arreange - Cria um livro e um capítulo
    from app.models.book import Book
    from app.models.chapter import Chapter

    book = Book(name="João", abbreviation="Jo")
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    book_id = book.id

    chapter = Chapter(number=3, book_id=book_id)
    db_session.add(chapter)
    db_session.commit()
    db_session.refresh(chapter)
    chapter_id = chapter.id

    # 2. Act - Cria um versículo
    verse_data = {
        "number": 16,
        "text": "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito...",
        "chapter_id": chapter_id,
    }
    response = client.post("/verses", json=verse_data)

    # 3. Assert - Verifica se foi criado
    assert response.status_code == 201
    data = response.json()
    assert data["number"] == 16
    assert "Deus amou o mundo" in data["text"]
    assert data["chapter_id"] == chapter_id
    assert "id" in data
