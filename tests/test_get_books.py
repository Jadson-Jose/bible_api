def test_list_all_books(client, db_session):
    # 1. Arrange - Cria alguns livros
    from app.models.book import Book

    book1 = Book(name="Gênesis", abbreviation="Gn")
    book2 = Book(name="Êxodo", abbreviation="Ex")
    book3 = Book(name="Levítico", abbreviation="Lv")

    db_session.add_all([book1, book2, book3])
    db_session.commit()

    # 2. Act - Busca todos os livros
    response = client.get("/books")

    # 3. Assert = Verifica a resposta
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Gênesis"
    assert data[1]["name"] == "Êxodo"
    assert data[2]["name"] == "Levítico"


def test_get_book_by_id(client, db_session):
    # 1. Arrange - Cria um livro
    from app.models.book import Book

    book = Book(name="Mateus", abbreviation="Mt")
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    book_id = book.id

    # 2. Act - Busca o livro pelo ID
    response = client.get(f"/books/{book_id}")

    # 3. Assert - Verifica a resposta
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id
    assert data["name"] == "Mateus"
    assert data["abbreviation"] == "Mt"


def test_get_book_not_found(client):
    # Tenta buscar um ID que não existe
    response = client.get("/books/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Livro não encontrado"
