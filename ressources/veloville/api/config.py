"""Chargement de la configuration depuis le fichier .env."""

import os

from dotenv import load_dotenv

# Charge les variables du fichier .env dans les variables d'environnement.
load_dotenv()

# Chaîne utilisée par SQLAlchemy pour se connecter à PostgreSQL.
DATABASE_URL = os.environ["DATABASE_URL"]

# Secret utilisé pour signer les JWT.
# Toute personne possédant ce secret pourrait fabriquer des tokens valides.
JWT_SECRET = os.environ["JWT_SECRET"]

# Algorithme de signature du JWT.
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Durée de validité d'un token.
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))