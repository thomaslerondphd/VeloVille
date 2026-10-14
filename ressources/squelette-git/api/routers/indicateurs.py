"""Routeur indicateurs.

À compléter : GET /indicateurs/activite-par-jour,
GET /indicateurs/stations-actives et
GET /indicateurs/incidents-par-statut.
"""
import math
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, select, case
from sqlalchemy.orm import Session
from datetime import date

from api.database import get_db
from api.models import Station, Incident, Trajet
from api.schemas import IndicateurActiviteResponse, ElementActiviteJour, IndicateurStationsActivesResponse, ElementStationActive, IndicateurIncidentsStatutResponse, ElementIncidentStatut
from api.dependencies import get_current_user, require_role
from api.schemas import UserResponse

router = APIRouter(
    prefix="/indicateurs",
    tags=["Indicateurs"],
    # dependencies=[Depends(get_current_user)],
    dependencies=[Depends(require_role(["direction", "exploitant"]))]
)


@router.get("/activite-par-jour", response_model=IndicateurActiviteResponse)
def lister_activite_par_jour(
    date_debut: Optional[date] = Query(default=None),
    date_fin: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
):
    
    """Retourne le nb de trajets par jour"""
    
    jour = func.date(Trajet.depart_horodatage).label("jour")

    stmt = select(
        jour.label("jour"),
        func.count(Trajet.trajet_id).label("nb_trajets"),
    ).group_by(jour)
    
    if date_debut:
        stmt = stmt.where(func.date(Trajet.depart_horodatage) >= date_debut)

    if date_fin:
        stmt = stmt.where(func.date(Trajet.depart_horodatage) <= date_fin)

    stmt = stmt.order_by(jour)
    resultats = db.execute(stmt).all()
    
    donnees = [
        ElementActiviteJour(
            jour=str(row.jour),
            nb_trajets=row.nb_trajets,
        )
        for row in resultats
    ]

    return IndicateurActiviteResponse(donnees=donnees)


@router.get("/stations-actives", response_model=IndicateurStationsActivesResponse)
def lister_stations_actives(
    limite: Optional[int] = Query(default=10, gt = 0),
    tri: str = Query(default="tout",description="Critère de tri : 'tout' (départs + arrivées), 'departs', ou 'arrivees'"),
    db: Session = Depends(get_db),
):
    
    """Retourne l'activité des stations trié par"""
    if tri not in ("tout", "departs", "arrivees"):
        raise HTTPException(status_code=422,detail="Le paramètre 'tri' doit être 'tout', 'departs' ou 'arrivees'")
    
    sous_total_departs = func.count(case((Trajet.station_depart == Station.station_id, 1)))
    sous_total_arrivees = func.count(case((Trajet.station_arrivee == Station.station_id, 1)))
    toute_activite = sous_total_arrivees + sous_total_departs
    
    if tri == "departs":
        ordre = sous_total_departs.desc()
    elif tri == "arrivees":
        ordre = sous_total_arrivees.desc()
    else:
        ordre = toute_activite.desc()
    
    stmt = (
        select(
            Station.station_id,
            Station.nom,
            sous_total_departs.label("nb_departs"),
            sous_total_arrivees.label("nb_arrivees"),
        )
        .join(
            Trajet,
            (Station.station_id == Trajet.station_depart)
            | (Station.station_id == Trajet.station_arrivee),
        )
        .group_by(Station.station_id, Station.nom)
        .order_by(ordre, Station.station_id.asc())
        .limit(limite)
    )
    
    resultats = db.execute(stmt).all()

    donnees = [
        ElementStationActive(
            station_id=row.station_id,
            nom=row.nom,
            nb_departs=row.nb_departs,
            nb_arrivees=row.nb_arrivees
        )
        for row in resultats
    ]

    return IndicateurStationsActivesResponse(donnees=donnees)


@router.get("/incidents-par-statut", response_model=IndicateurIncidentsStatutResponse)
def indicateur_incidents_statut(db: Session = Depends(get_db)):
    
    """Retourne la répartition des incidents par statut et le délai moyen de résolution en heures."""
    stmt_comptage = select(
        Incident.statut,
        func.count(Incident.incident_id).label("nb_incidents"),
    ).group_by(Incident.statut)

    rows_comptage = db.execute(stmt_comptage).all()

    donnees = [
        ElementIncidentStatut(
            statut=row.statut,
            nb_incidents=row.nb_incidents,
        )
        for row in rows_comptage
    ]

    stmt_delai_moy = select(
        func.avg(
            func.extract("epoch", Incident.date_resolution - Incident.date_signalement) / 3600.0
        )
    ).where(
        Incident.statut == "resolu",
        Incident.date_resolution.is_not(None),
    )

    delai_moyen_valeur = db.scalar(stmt_delai_moy)
    delai_moyen = (
        round(float(delai_moyen_valeur), 2)
        if delai_moyen_valeur is not None
        else None
    )

    return IndicateurIncidentsStatutResponse(
        donnees=donnees,
        delai_moyen_resolution_heures=delai_moyen,
    )