"""Routeur trajets.

À compléter : GET /trajets (filtres date_debut, date_fin, station ; pagination).
"""
import math
from datetime import date, datetime, time
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.database import get_db
from api.dependencies import get_current_user
from api.models import Trajet
from api.schemas import PaginatedTrajetsResponse

router = APIRouter(
    prefix="/trajets",
    tags=["Trajets"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=PaginatedTrajetsResponse)
def lister_trajets(
    date_debut: Optional[date] = Query(default=None),
    date_fin: Optional[date] = Query(default=None),
    station: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Affiche la liste paginée des trajets avec filtres optionnels sur les dates et la station."""
    stmt_base = select(Trajet)
    stmt_count = select(func.count()).select_from(Trajet)

    # Filtrage par plage de dates (inclusive)
    if date_debut:
        dt_debut = datetime.combine(date_debut, time.min)
        stmt_base = stmt_base.where(Trajet.depart_horodatage >= dt_debut)
        stmt_count = stmt_count.where(Trajet.depart_horodatage >= dt_debut)

    if date_fin:
        dt_fin = datetime.combine(date_fin, time.max)
        stmt_base = stmt_base.where(Trajet.depart_horodatage <= dt_fin)
        stmt_count = stmt_count.where(Trajet.depart_horodatage <= dt_fin)

    # Filtrage si la station demandée est soit la station de départ, soit d'arrivée
    if station:
        condition_station = (Trajet.station_depart == station) | (
            Trajet.station_arrivee == station
        )
        stmt_base = stmt_base.where(condition_station)
        stmt_count = stmt_count.where(condition_station)

    total = db.scalar(stmt_count) or 0
    pages = math.ceil(total / taille_page) if total else 0
    offset = (page - 1) * taille_page

    trajets = db.scalars(
        stmt_base.order_by(Trajet.depart_horodatage.asc())
        .offset(offset)
        .limit(taille_page)
    ).all()

    return PaginatedTrajetsResponse(
        total=total,
        page=page,
        taille_page=taille_page,
        pages=pages,
        resultats=trajets,
    )