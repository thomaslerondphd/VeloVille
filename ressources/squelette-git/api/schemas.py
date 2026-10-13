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
    """Utilisateur retourné par l'API (lecture / authentification) sans identifiant SQL."""

    model_config = ConfigDict(from_attributes=True)

    username: str
    role: str


class UserCreate(BaseModel):
    """Payload pour la création / inscription d'un nouvel utilisateur (l'id sera généré par la BDD)."""

    username: str
    password: str
    role: str


class UserInDB(UserResponse):
    """Modèle représentant l'utilisateur stocké en base de données avec son ID généré."""

    user_id: int


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

# Enveloppe de Pagination Générique


class PaginatedResponse(BaseModel):
    """Enveloppe paginée universelle pour les listes de ressources."""
    
    model_config = ConfigDict(from_attributes=True)
    
    total: int
    page: int
    taille_page: int
    resultats: List[Any]

class PaginatedStationResponse(BaseModel):
    """Enveloppe paginée spécifique aux stations."""

    total: int
    page: int
    taille_page: int
    pages: int
    resultats: List[StationResponse]

# Indicateurs Clés de Performance

class ElementActiviteJour(BaseModel):
    jour: str
    nb_trajets: int


class IndicateurActiviteResponse(BaseModel):
    donnees: List[ElementActiviteJour]


class ElementStationActive(BaseModel):
    station_id: str
    nom: str
    nb_departs: int
    nb_arrivees: int


class IndicateurStationsActivesResponse(BaseModel):
    donnees: List[ElementStationActive]


class ElementIncidentStatut(BaseModel):
    statut: str
    nb_incidents: int


class IndicateurIncidentsStatutResponse(BaseModel):
    donnees: List[ElementIncidentStatut]
    delai_moyen_resolution_heures: Optional[float] = None