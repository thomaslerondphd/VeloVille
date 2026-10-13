from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET


def hash_password(plain_password: str) -> str:
    """Transforme un mot de passe en hash bcrypt avant stockage en base."""

    # gensalt() génère un sel aléatoire intégré directement dans le hash bcrypt.
    salt = bcrypt.gensalt()

    # hashpw() produit le hash à partir du mot de passe + du sel.
    hashed = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        salt,
    )

    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe saisi correspond au hash stocké."""

    # checkpw() refait le calcul bcrypt avec les informations contenues dans le hash.
    # On ne déchiffre donc jamais le mot de passe enregistré.
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(username: str) -> str:
    """Crée un JWT signé pour l'utilisateur authentifié."""

    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=JWT_EXPIRE_MINUTES)

    payload = {
        # sub ("subject") identifie l'utilisateur auquel appartient le token.
        "sub": username,

        # iat indique quand le token a été créé.
        "iat": now,

        # exp fixe la date après laquelle le token n'est plus accepté.
        "exp": expiration,
    }

    # encode() signe le contenu avec JWT_SECRET.
    # Le token peut être lu, mais une modification casserait sa signature.
    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """Vérifie la signature et l'expiration puis retourne le payload."""

    # decode() refuse un token modifié, mal signé ou expiré.
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[JWT_ALGORITHM],
    )