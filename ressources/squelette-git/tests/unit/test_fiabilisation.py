"""Tests unitaires des règles de fiabilisation.

À compléter : un test par règle, cas nominal et cas de rejet.
"""
"""Tests unitaires des règles de fiabilisation.

Un test par règle : cas nominal et cas de rejet.
"""
"""Tests unitaires des règles de fiabilisation.

Un test par règle, cas nominal, cas d'avertissement (normalisation) et cas de rejet.
"""

import pytest
from datetime import datetime
from api.services.fiabilisation import (
    fiabiliser_station,
    fiabiliser_trajet,
    fiabiliser_incident,
    valider_horodatage,
    valider_expression_reguliere
)


# --- 1. TESTS DE BASE (HORODATAGE & REGEX) ---

def test_valider_horodatage_nominal():
    """Vérifie le format nominal d'un horodatage ISO."""
    resultat = valider_horodatage("2026-08-26 20:00:00")
    assert resultat["erreur"] is None
    assert isinstance(resultat["valeur"], datetime)


def test_valider_horodatage_rejet():
    """Vérifie le rejet d'un format de date non reconnu (ex: format FR avec slashes invalides)."""
    resultat = valider_horodatage("24/08/2026 11:01")
    assert resultat["erreur"] is not None


def test_valider_expression_reguliere_normalisation():
    """Vérifie la normalisation de la casse d'un identifiant (ex: v1281 -> V1281)."""
    resultat = valider_expression_reguliere("v1281", r"^V[0-9]{4}$", "velo_id")
    assert resultat["erreur"] is None
    assert resultat["valeur"] == "V1281"
    assert resultat["avertissement"] is not None


# --- 2. TESTS DES STATIONS ---

def test_fiabiliser_station_nominal():
    """Vérifie le cas nominal d'une station valide."""
    ligne = {
        "station_id": "S001",
        "nom": "Gare Centrale",
        "commune": "Lille",
        "capacite": "30",
        "latitude": "50.633",
        "longitude": "3.058",
        "date_mise_en_service": "2025-01-01"
    }
    res = fiabiliser_station(ligne)
    assert res["erreur"] is None
    assert res["donnees"]["station_id"] == "S001"
    assert res["donnees"]["capacite"] == 30


def test_fiabiliser_station_rejet_capacite():
    """Vérifie le rejet d'une station dont la capacité est négative ou nulle."""
    ligne = {
        "station_id": "S001",
        "nom": "Gare",
        "commune": "Lille",
        "capacite": "0",
        "latitude": "50.633",
        "longitude": "3.058",
        "date_mise_en_service": "2025-01-01"
    }
    res = fiabiliser_station(ligne)
    assert res["erreur"] is not None


# --- 3. TESTS DES TRAJETS ---

def test_fiabiliser_trajet_nominal_avec_avertissement():
    """Vérifie un trajet valide avec un avertissement de normalisation (vélo_id en minuscules)."""
    stations_valides = {"S001", "S002"}
    ligne = {
        "trajet_id": "T000001",
        "velo_id": "v1281",  # Cas issu du journal (Ligne 89)
        "depart_horodatage": "2026-08-26 10:00:00",
        "station_depart": "S001",
        "station_arrivee": "S002",
        "duree_secondes": "300",
        "type_usager": "abonne",
        "usager_ref": "U12345678"
    }
    res = fiabiliser_trajet(ligne, stations_valides)
    assert res["erreur"] is None
    assert res["donnees"]["velo_id"] == "V1281"  # Normalisé en majuscule
    assert res["avertissement"] is not None


def test_fiabiliser_trajet_rejet_station_inconnue():
    """Vérifie le rejet d'un trajet avec une station d'arrivée inconnue (ex: S999)."""
    stations_valides = {"S001"}
    ligne = {
        "trajet_id": "T000002",
        "velo_id": "V1281",
        "depart_horodatage": "2026-08-26 10:00:00",
        "station_depart": "S001",
        "station_arrivee": "S999",  # Station inconnue (Ligne 31 du journal)
        "duree_secondes": "300",
        "type_usager": "abonne",
        "usager_ref": ""
    }
    res = fiabiliser_trajet(ligne, stations_valides)
    assert res["erreur"] is not None
    assert "station" in res["erreur"].lower()


def test_fiabiliser_trajet_rejet_duree_negative():
    """Vérifie le rejet d'un trajet dont la durée est négative (ex: -120)."""
    stations_valides = {"S001", "S002"}
    ligne = {
        "trajet_id": "T000003",
        "velo_id": "V1281",
        "depart_horodatage": "2026-08-26 10:00:00",
        "station_depart": "S001",
        "station_arrivee": "S002",
        "duree_secondes": "-120",  # Cas issu du journal (Ligne 601)
        "type_usager": "abonne",
        "usager_ref": ""
    }
    res = fiabiliser_trajet(ligne, stations_valides)
    assert res["erreur"] is not None
    assert "duree_secondes" in res["erreur"]


# --- 4. TESTS DES INCIDENTS ---

def test_fiabiliser_incident_nominal_avec_correction_statut():
    """Vérifie la normalisation d'un incident avec le statut 'en cours' corrigé en 'en_cours'."""
    stations_valides = {"S001"}
    ligne = {
        "incident_id": "I2026-0001",
        "date_signalement": "2026-08-26 10:00:00",
        "cible": "station",
        "velo_id": "",
        "station_id": "S001",
        "type_incident": "Panne borne",
        "statut": "en cours",  # Cas issu du journal (Ligne 2)
        "date_resolution": "",
        "technicien": "Alice"
    }
    res = fiabiliser_incident(ligne, stations_valides)
    assert res["erreur"] is None
    assert res["donnees"]["statut"] == "en_cours"  # Normalisé
    assert res["avertissement"] is not None


def test_fiabiliser_incident_rejet_coherence_dates():
    """Vérifie le rejet d'un incident dont la date de résolution est antérieure au signalement."""
    stations_valides = {"S001"}
    ligne = {
        "incident_id": "I2026-0002",
        "date_signalement": "2026-08-26 10:00:00",
        "cible": "station",
        "velo_id": "",
        "station_id": "S001",
        "type_incident": "Panne",
        "statut": "resolu",
        "date_resolution": "2026-08-25 10:00:00",  # Antérieure (Ligne 29 du journal)
        "technicien": "Bob"
    }
    res = fiabiliser_incident(ligne, stations_valides)
    assert res["erreur"] is not None
    assert "antérieure" in res["erreur"]