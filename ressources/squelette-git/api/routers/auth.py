"""Routeur auth.

À compléter : POST /auth/login.
"""
"""Endpoint responsable de l'authentification."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Utilisateur
from api.schemas import LoginRequest, TokenResponse, RegisterRequest
from api.securite import create_access_token, verify_password, hash_password

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Vérifie l'utilisateur en base puis délivre un JWT."""

    # Recherche l'utilisateur dont le username correspond à celui reçu.
    user = db.scalar(
        select(Utilisateur).where(Utilisateur.username == data.username)
    )

    # On garde le même message pour "utilisateur inconnu" et "mauvais mot de passe".
    # Cela évite de révéler quels usernames existent réellement dans la base.
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )

    # Le mot de passe n'est utilisé que pendant le login.
    # Une fois authentifié, l'utilisateur reçoit un token.
    token = create_access_token(user.username)

    return TokenResponse(access_token=token)



@router.post("/register", status_code=201)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    # Vérifie qu'un utilisateur avec ce username n'existe pas déjà.
    existing_user = db.scalar(
        select(Utilisateur).where(Utilisateur.username == data.username)
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Nom d'utilisateur déjà utilisé",
        )

    # Le mot de passe est haché avant d'être enregistré en base.
    user = Utilisateur(
        username=data.username,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.user_id,
        "username": user.username,
    }