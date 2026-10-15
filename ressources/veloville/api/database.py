"""Connexion à PostgreSQL (SQLAlchemy 2).

À compléter : lire DATABASE_URL depuis l'environnement (.env), créer l'engine, la
fabrique de sessions et la dépendance get_db() utilisée par les routeurs.
"""
"""Configuration de la connexion PostgreSQL avec SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api.config import DATABASE_URL

# L'engine représente la connexion générale entre SQLAlchemy et PostgreSQL.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Vérifie qu'une connexion du pool est encore valide avant usage.
)

# Fabrique de sessions : chaque requête utilisera sa propre Session SQLAlchemy.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Classe de base dont héritent les modèles SQLAlchemy."""
    pass


def get_db():
    """Fournit une session SQLAlchemy à FastAPI puis la ferme proprement."""

    db = SessionLocal()

    try:
        # yield permet à FastAPI d'injecter la session dans l'endpoint.
        yield db
    finally:
        # La session est fermée même si l'endpoint provoque une erreur.
        db.close()