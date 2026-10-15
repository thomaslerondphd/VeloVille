"""Fixtures pytest communes.

À compléter : client TestClient de l'API, jetons pour exploitant01 et direction01,
session de base de données de test. Aucun secret en dur : lire .env.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


from api.database import Base, get_db
from api.main import app
from api.models import Utilisateur
from api.securite import hash_password


load_dotenv()

DATABASE_URL_TEST = os.getenv(
    "DATABASE_URL_TEST",
)

engine = create_engine(DATABASE_URL_TEST, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Initialise la base de données et crée les utilisateurs nécessaires au login."""
    Base.metadata.create_all(bind=engine)
    connexion = engine.connect()
    transaction = connexion.begin()
    session = TestingSessionLocal(bind=connexion, join_transaction_mode="create_savepoint")
    
    if not session.query(Utilisateur).filter(Utilisateur.username == "exploitant01").first():
        session.add(
            Utilisateur(
                username="exploitant01",
                mot_de_passe_hash=hash_password("Formation2026!"),
                role="exploitant",
            )
        )
    if not session.query(Utilisateur).filter(Utilisateur.username == "direction01").first():
        session.add(
            Utilisateur(
                username="direction01",
                mot_de_passe_hash=hash_password("Formation2026!"),
                role="direction",
            )
        )
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connexion.close()

@pytest.fixture(scope="function")
def db_session():
    """Ouvre une transaction isolée et fait un rollback à la fin du test."""
    connexion = engine.connect()
    transaction = connexion.begin()
    session = TestingSessionLocal(bind=connexion, join_transaction_mode="create_savepoint")

    yield session

    session.close()
    transaction.rollback()
    connexion.close()


@pytest.fixture(scope="function")
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    
def _login_and_get_token(
    client: TestClient,
    username: str,
    password: str,
) -> str:
    """Effectue un vrai login comme le ferait un client de l'API."""

    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture(scope="function")
def exploitant_token(client):
    """JWT appartenant à un utilisateur exploitant."""

    return _login_and_get_token(
        client,
        "exploitant01",
        "Formation2026!",
    )


@pytest.fixture(scope="function")
def direction_token(client):
    """JWT appartenant à un utilisateur direction."""

    return _login_and_get_token(
        client,
        "direction01",
        "Formation2026!",
    )
    
