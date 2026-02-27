def test_list_verses_by_chapter(client, db_session):
    # 1. Arrange - Cria livro, capítulo e versículos
    from app.models.book import Book
    from app.models.chapter import Chapter
    from app.models.verse import Verse

    book = Book(name="Joao", abbreviation="Jo")
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    chapter = Chapter(number=3, book_id=book.id)
    db_session.add(chapter)
    db_session.commit()
    db_session.refresh(chapter)

    verse1 = Verse(
        number=16,
        text="Porque Deus amou o mundo...",
        chapter_id=chapter.id,
    )
    verse2 = Verse(
        number=17,
        text="Porque Deus eviou o seu filho...",
        chapter_id=chapter.id,
    )

    db_session.add_all([verse1, verse2])
    db_session.commit()

    # 2. Act - Busca versículos do capítulo
    response = client.get(f"/chapters/{chapter.id}/verses")

    # 3. Assert - Verifica a resposta
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["number"] == 16
    assert "Deus amou" in data[0]["text"]
    assert data[1]["number"] == 17
    assert all(v["chapter_id"] == chapter.id for v in data)


def test_search_verses_by_text(client, db_session):
    # 1. Arrange - Cria alguns versículos
    from app.models.book import Book
    from app.models.chapter import Chapter
    from app.models.verse import Verse

    book = Book(name="João", abbreviation="Jo")
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    chapter = Chapter(number=1, book_id=book.id)
    db_session.add(chapter)
    db_session.commit()
    db_session.refresh(chapter)

    verse1 = Verse(
        number=1,
        text="No princípio era o Verbo",
        chapter_id=chapter.id,
    )
    verse2 = Verse(
        number=2,
        text="E o Verbo estava com Deus",
        chapter_id=chapter.id,
    )
    verse3 = Verse(
        number=3,
        text="Todas as coisas foram feitas por ele",
        chapter_id=chapter.id,
    )

    db_session.add_all([verse1, verse2, verse3])
    db_session.commit()

    # 2. Act - Busca versículos com a palavra "Verbo"
    response = client.get("/verses?search=Verbo")

    # 3. Assert - Verifica que encontrou 2 versículos
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "Verbo" in data[0]["text"]
    assert "Verbo" in data[1]["text"]

    # 4. Busca que não encontra nada
    response = client.get("/verses?search=inexistente")
    assert response.status_code == 200
    assert len(response.json()) == 0
