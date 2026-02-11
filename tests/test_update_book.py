def test_update_book(client, db_session):
    # 1 Arrage - Cria um livro primeiro
    from app.models.book import Book

    book = Book(name="Livro Original", abbreviation="LO")
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    book_id = book.id

    # 2. Act - Atualiza o livro
    update_data = {"name": "Livro Atualizado", "abbreviation": "LA"}
    response = client.put(f"/books/{book_id}", json=update_data)

    # 3. Assert = Verifica se foi atualizado
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["name"] == "Livro Atualizado"
    assert data["abbreviation"] == "LA"

    # Verifica no banco
    updated_book = db_session.query(Book).filter(Book.id == book.id).first()
    assert updated_book.name == "Livro Atualizado"
    assert updated_book.abbreviation == "LA"
