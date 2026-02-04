from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_book_with_valid_data():
    # 1. Arrange (Preparar)
    book_data = {"name": "Gênesis", "abbreviation": "Gn"}

    # 2. Act (Agir)
    response = client.post("/books", json=book_data)

    # 3. Assert (Verificar)
    assert response.status_code == 201
    assert response.json()["name"] == "Gênesis"
    assert response.json()["abbreviation"] == "Gn"
    assert "id" in response.json()
