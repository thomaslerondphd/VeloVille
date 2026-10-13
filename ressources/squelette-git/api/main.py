"""Point d'entrée de l'API VéloVille (FastAPI).

À compléter : créer l'application, inclure les routeurs (auth, stations, trajets,
incidents, indicateurs) et exposer GET /sante -> {"statut": "ok"}.

Lancement : uvicorn api.main:app --reload
"""
"""Point d'entrée principal de l'API."""

from fastapi import FastAPI

from api.routers import auth

app = FastAPI(
    title="VéloVille",
    description="L'application de gestion des vélos en libre-service de la ville",
    version="0.1.0",
)

app.include_router(auth.router)
# app.include_router(demo.router)


@app.get("/", tags=["Accueil"])
def root():
    """Confirme simplement que l'API fonctionne."""
    return {
        "message": "API démarrée",
        "documentation": "/docs",
    }

@app.get("/sante", tags=["Santé"])
def verifier_sante():
    return {"statut": "OK"}
# python -m uvicorn app.main:app --reload