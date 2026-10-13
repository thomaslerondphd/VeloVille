"""Schémas Pydantic (entrées et sorties de l'API).

À compléter : schémas de lecture des trois ressources, enveloppe paginée, corps de
connexion, réponse de connexion, corps de changement de statut, réponses
des trois indicateurs.
"""
from datetime import date, datetime
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict

# Authentification et Utilisateurs

class LoginRequest(BaseModel):
    """Données envoyées par le client lors de la connexion."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Réponse renvoyée après une authentification réussie."""

    access_token: str
    token_type: str = "bearer"
    role: str


class UserResponse(BaseModel):
    """Utilisateur exposé par l'API sans jamais révéler password_hash."""

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    role: str


class RegisterRequest(BaseModel):
    """Payload pour l'inscription / création d'un utilisateur."""

    username: str
    password: str
    role: str

# Restitution Métier (Stations, Trajets, Incidents)

class StationResponse(BaseModel):
    """Représentation d'une station."""

    model_config = ConfigDict(from_attributes=True)

    station_id: str
    nom: str
    commune: str
    capacite: int
    latitude: float
    longitude: float


class TrajetResponse(BaseModel):
    """Représentation d'un trajet."""

    model_config = ConfigDict(from_attributes=True)

    trajet_id: str
    velo_id: str
    station_depart: str
    station_arrivee: Optional[str] = None
    depart_horodatage: datetime
    duree_secondes: int
    type_usager: str
    usager_ref: Optional[str] = None


class IncidentResponse(BaseModel):
    """Représentation d'un incident."""

    model_config = ConfigDict(from_attributes=True)

    incident_id: str
    cible: str
    velo_id: Optional[str] = None
    station_id: Optional[str] = None
    statut: str
    date_signalement: datetime
    date_resolution: Optional[datetime] = None
    technicien: Optional[str] = None


class IncidentUpdateStatut(BaseModel):
    """Payload de mise à jour du statut d'un incident."""

    statut: str
