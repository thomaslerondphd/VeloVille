"""Routeur incidents.

À compléter : GET /incidents (filtre statut, pagination) et
PUT /incidents/{incident_id}/statut (rôle exploitant).
"""
import math
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
import datetime

from api.database import get_db
from api.models import Incident
from api.schemas import PaginatedResponse, IncidentResponse, PaginatedIncidentsResponse, IncidentUpdateStatut
from api.dependencies import get_current_user
from api.schemas import UserResponse

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=PaginatedIncidentsResponse)
def lister_incidents(
    commune: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Affiche la liste paginée des stations (mode lecture seule)."""
    stmt_base = select(Incident)
    stmt_count = select(func.count()).select_from(Incident)

    if commune:
        stmt_base = stmt_base.where(Incident.commune == commune)
        stmt_count = stmt_count.where(Incident.commune == commune)

    total = db.scalar(stmt_count) or 0
    pages = math.ceil(total / taille_page) if total else 0
    offset = (page - 1) * taille_page

    incidents = db.scalars(
        stmt_base.order_by(Incident.incident_id.asc())
        .offset(offset)
        .limit(taille_page)
    ).all()

    return PaginatedIncidentsResponse(
        total=total,
        page=page,
        taille_page=taille_page,
        pages=pages,
        resultats=incidents,
    )

@router.put("/{incident_id}/statut", response_model=IncidentResponse)
def mise_a_jour_incident(incident_id, payload: IncidentUpdateStatut, db: Session = Depends(get_db)):
    incident = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
    
    if not incident :
        raise HTTPException(status_code=404, detail="incident introuvable")
    
    modif_valides = {
    "ouvert": ["en_cours", "resolu"],
    "en_cours": ["resolu"],
    "resolu": [],
    }
    
    statut_actuel = incident.statut
    nouveau_statut = payload.statut

    if nouveau_statut not in modif_valides.get(statut_actuel, []):
        raise HTTPException(status_code=422, detail="Modification non autorisée")

    incident.statut = nouveau_statut

    # Renseignement automatique de date_resolution
    if nouveau_statut == "resolu" and not incident.date_resolution:
        incident.date_resolution = datetime.now()

    db.commit()
    db.refresh(incident)

    return incident