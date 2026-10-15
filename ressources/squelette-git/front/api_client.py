"""Client HTTP centralisé vers l'API VéloVille.

À compléter : lire API_URL et API_TIMEOUT_SECONDES, ajouter l'en-tête
Authorization: Bearer <jeton>, lever ErreurApi (message en français)
sur erreur réseau, délai dépassé ou code HTTP d'erreur.
"""

import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL")
API_TIMEOUT_SECONDES = int(os.getenv("API_TIMEOUT_SECONDES", "5"))


class ErreurApi(Exception):
    """Exception personnalisée levée lors des erreurs d'appel API."""

    pass


def appeler_api(
    methode: str,
    endpoint: str,
    params: dict = None,
    json_data: dict = None,
    auth_requis: bool = True,
) -> dict:
    """Effectue une requête HTTP vers l'API et retourne le JSON sous forme de dictionnaire."""
    headers = {}

    if auth_requis:
        token = st.session_state.get("jwt_token")
        if not token:
            raise ErreurApi("Authentification requise. Veuillez vous connecter.")
        headers["Authorization"] = f"Bearer {token}"

    url = f"{API_URL.rstrip('/')}{endpoint}"

    try:
        reponse = requests.request(
            method=methode,
            url=url,
            params=params,
            json=json_data,
            headers=headers,
            timeout=API_TIMEOUT_SECONDES,
        )

        if reponse.status_code in (200, 201):
            return reponse.json()

        # Traitement des erreurs renvoyées par FastAPI
        try:
            detail = reponse.json().get("detail")
            if detail:
                raise ErreurApi(f"Erreur API ({reponse.status_code}) : {detail}")
        except ValueError:
            pass

        raise ErreurApi(f"Erreur serveur (code HTTP {reponse.status_code}).")

    except requests.exceptions.Timeout:
        raise ErreurApi("Délai d'attente dépassé lors de la connexion à l'API.")
    except requests.exceptions.RequestException as e:
        raise ErreurApi(f"Impossible de contacter l'API : {str(e)}")

