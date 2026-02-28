import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db


# Base de datos exclusiva para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Crear todas las tablas antes de correr tests
Base.metadata.create_all(bind=engine)


# Override de dependencia de DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Fixture principal
@pytest.fixture
def client():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    return TestClient(app)


# Helper para autenticación en tests
def create_user_and_get_token(client, email="test@test.com", password="123456"):
    # Registrar usuario
    client.post("/api/auth/register", json={
        "email": email,
        "password": password
    })

    # Login
    response = client.post("/api/auth/login", data={
        "username": email,
        "password": password
    })

    return response.json()["access_token"]