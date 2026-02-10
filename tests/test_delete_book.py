def test_delete_book(client, db_session):
    # 1. Arrange - Cria um livro primeiro
    from app.models.book import Book

    book = Book(name="Livro para Deletar", abbreviation="LpD")
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    book_id = book.id

    # 2. Act - Deleta o livro
    response = client.delete(f"/books/{book_id}")

    # 3. Assert - Verifica se foi deletado
    assert response.status_code == 204  # 204 = No Content (secesso sem retorno)

    # Verifica se realmente foi deletado no banco
    delete_book = db_session.query(Book).filter(Book.id == book_id).first()
    assert delete_book is None
