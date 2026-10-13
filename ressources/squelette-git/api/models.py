"""Modèles ORM SQLAlchemy : Station, Trajet, Incident, Utilisateur.

À compléter : déclarer les quatre tables conformément à sql/schema.sql.
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from api.database import Base


class Station(Base):
    __tablename__ = "stations"

    station_id = Column(String, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    commune = Column(String, nullable=False)
    capacite = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class Trajet(Base):
    __tablename__ = "trajets"

    trajet_id = Column(String, primary_key=True, index=True)
    station_depart = Column(String, ForeignKey("stations.station_id"), nullable=False)
    station_arrivee = Column(String, ForeignKey("stations.station_id"), nullable=True)
    depart_horodatage = Column(DateTime, nullable=False, index=True)
    duree_secondes = Column(Integer, nullable=False)
    type_usager = Column(String, nullable=False)
    usager_ref = Column(String, nullable=True)


class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(String, primary_key=True, index=True)
    cible = Column(String, nullable=False)
    velo_id = Column(String, nullable=True)
    station_id = Column(String, ForeignKey("stations.station_id"), nullable=True)
    statut = Column(String, nullable=False)
    date_signalement = Column(DateTime, nullable=False, index=True)
    date_resolution = Column(DateTime, nullable=True)
    technicien = Column(String, nullable=True)
    
class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    mot_de_passe_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)