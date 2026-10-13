from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    mot_de_passe_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("role IN ('direction', 'exploitant')", name="chk_role"),
    )


class Station(Base):
    __tablename__ = "stations"

    station_id: Mapped[str] = mapped_column(String(4), primary_key=True, index=True)
    nom: Mapped[str] = mapped_column(String, nullable=False)
    commune: Mapped[str] = mapped_column(String, nullable=False)
    capacite: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)


class Trajet(Base):
    __tablename__ = "trajets"

    trajet_id: Mapped[str] = mapped_column(String(7), primary_key=True, index=True)
    velo_id: Mapped[str] = mapped_column(String(5), nullable=False)
    station_depart: Mapped[str] = mapped_column(String(4), ForeignKey("stations.station_id"), nullable=False)
    station_arrivee: Mapped[Optional[str]] = mapped_column(String(4), ForeignKey("stations.station_id"), nullable=True)
    depart_horodatage: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    duree_secondes: Mapped[int] = mapped_column(Integer, nullable=False)
    type_usager: Mapped[str] = mapped_column(String(10), nullable=False)
    usager_ref: Mapped[Optional[str]] = mapped_column(String(9), nullable=True)


class Incident(Base):
    __tablename__ = "incidents"

    incident_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    cible: Mapped[str] = mapped_column(String, nullable=False)
    velo_id: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    station_id: Mapped[Optional[str]] = mapped_column(String(4), ForeignKey("stations.station_id"), nullable=True)
    statut: Mapped[str] = mapped_column(String, nullable=False)
    date_signalement: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    date_resolution: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    technicien: Mapped[Optional[str]] = mapped_column(String, nullable=True)