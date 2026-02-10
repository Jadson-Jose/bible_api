import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE não encontrada no arquivo .env")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco para cada teste e limpa após o teste"""
    print("\n🔧 Criando tabelas...")
    # Recria as tabelas do zero (garante que está limpo)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas!")

    # Cria sessão
    session = TestingSessionLocal()

    yield session

    print("🧹 Limpando após o teste...")
    # Limpa após o teste
    session.close()

    # Drop e recria para garantir limpeza total
    Base.metadata.drop_all(bind=engine)
    print("✅ Limpeza concluída!")


@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de teste que usa o banco de testes"""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
