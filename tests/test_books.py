import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_book_with_valid_data():
    # 1. Arrange (Preparar)
    unique_suffix = f"Livro_{uuid.uuid4().hex[:6]}"
    book_data = {
        "name": f"Livro_Test_{unique_suffix}",
        "abbreviation": "TST",
    }

    # 2. Act (Agir)
    response = client.post("/books", json=book_data)

    # 3. Assert (Verificar)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == book_data["name"]
    assert data["abbreviation"] == "TST"
    assert "id" in data
