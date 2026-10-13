import math
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Station
from api.schemas import PaginatedResponse, StationResponse, PaginatedStationResponse
from api.dependencies import get_current_user
from api.schemas import UserResponse

router = APIRouter(
    prefix="/stations",
    tags=["Stations"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=PaginatedStationResponse)
def lister_stations(
    commune: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Affiche la liste paginée des stations (mode lecture seule)."""
    stmt_base = select(Station)
    stmt_count = select(func.count()).select_from(Station)

    if commune:
        stmt_base = stmt_base.where(Station.commune == commune)
        stmt_count = stmt_count.where(Station.commune == commune)

    total = db.scalar(stmt_count) or 0
    pages = math.ceil(total / taille_page) if total else 0
    offset = (page - 1) * taille_page

    stations = db.scalars(
        stmt_base.order_by(Station.station_id.asc())
        .offset(offset)
        .limit(taille_page)
    ).all()

    return PaginatedStationResponse(
        total=total,
        page=page,
        taille_page=taille_page,
        pages=pages,
        resultats=stations,
    )


@router.get("/{station_id}", response_model=StationResponse)
def lire_station(
    station_id: str,
    db: Session = Depends(get_db),
):
    """Retourne les détails d'une station à partir de son identifiant."""
    station = db.scalar(
        select(Station).where(Station.station_id == station_id)
    )

    if not station:
        raise HTTPException(status_code=404, detail="Station introuvable")

    return station