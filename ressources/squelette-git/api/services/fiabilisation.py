"""Règles de fiabilisation des données (module métier testé).

À compléter : fonctions pures, sans accès à la base, qui normalisent ou rejettent
une valeur ou une ligne : horodatages, identifiants de vélo, statuts
d'incident, durées, références de station, cohérence des dates,
doublons. Chaque fonction retourne la valeur normalisée ou signale le
motif de rejet. Ces fonctions sont appelées par scripts/importer.py et
couvertes par tests/unit/.
"""
import re
from datetime import datetime


def valider_horodatage(valeur):
    """Valide et transforme une date ou un horodatage ( ISO : AAAA-MM-JJ [HH:MM:SS] )."""
    if not valeur or str(valeur).strip().lower() in ("", "nan", "none", "null"):
        return {"valeur": None, "erreur": None}
    valeur_texte = str(valeur).strip()
    formats_acceptes = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]
    for format_date in formats_acceptes:
        try:
            date_analysee = datetime.strptime(valeur_texte, format_date)
            return {"valeur": date_analysee, "erreur": None}
        except ValueError:
            continue
    return {"valeur": None, "erreur": f"Format d'horodatage invalide : '{valeur}'"}


def valider_expression_reguliere(valeur, motif, nom_du_champ, optionnel=False):
    """Vérifie qu'une chaîne respecte un motif de texte précis - Regex."""
    if not valeur or str(valeur).strip().lower() in ("", "nan", "none", "null"):
        if optionnel:
            return {"valeur": None, "erreur": None}
        return {"valeur": None, "erreur": f"Le champ '{nom_du_champ}' est obligatoire."}
    
    valeur_texte = str(valeur).strip()
    if not re.match(motif, valeur_texte):
        return {"valeur": None, "erreur": f"Format invalide pour {nom_du_champ} ('{valeur_texte}')"}
    return {"valeur": valeur_texte, "erreur": None}


def fiabiliser_station(ligne):
    """Valide et normalise une ligne de la table des stations."""
    nettoyage_id = valider_expression_reguliere(ligne.get("station_id"), r"^S[0-9]{3}$", "station_id")
    if nettoyage_id["erreur"]:
        return {"donnees": None, "erreur": nettoyage_id["erreur"]}

    try:
        capacite = int(ligne.get("capacite", 0))
        if capacite <= 0:
            return {"donnees": None, "erreur": f"La capacité doit être > 0 (valeur: {ligne.get('capacite')})"}
    except (ValueError, TypeError):
        return {"donnees": None, "erreur": f"Capacité invalide : '{ligne.get('capacite')}'"}

    nettoyage_date = valider_horodatage(ligne.get("date_mise_en_service"))
    if nettoyage_date["erreur"] or not nettoyage_date["valeur"]:
        return {"donnees": None, "erreur": nettoyage_date["erreur"] or "La date de mise en service est obligatoire."}

    try:
        latitude = round(float(ligne.get("latitude")), 5)
        longitude = round(float(ligne.get("longitude")), 5)
    except (ValueError, TypeError):
        return {"donnees": None, "erreur": "Coordonnées latitude/longitude invalides."}

    return {
        "donnees": {
            "station_id": nettoyage_id["valeur"],
            "nom": str(ligne.get("nom", "")).strip(),
            "commune": str(ligne.get("commune", "")).strip(),
            "capacite": capacite,
            "latitude": latitude,
            "longitude": longitude,
            "date_mise_en_service": nettoyage_date["valeur"].date(),
        },
        "erreur": None
    }


def fiabiliser_trajet(ligne, ensemble_stations_valides):
    """Valide et normalise une ligne de la table des trajets."""
    nettoyage_trajet_id = valider_expression_reguliere(ligne.get("trajet_id"), r"^T[0-9]{6}$", "trajet_id")
    if nettoyage_trajet_id["erreur"]:
        return {"donnees": None, "erreur": nettoyage_trajet_id["erreur"]}

    nettoyage_velo_id = valider_expression_reguliere(ligne.get("velo_id"), r"^V[0-9]{4}$", "velo_id")
    if nettoyage_velo_id["erreur"]:
        return {"donnees": None, "erreur": nettoyage_velo_id["erreur"]}

    nettoyage_depart = valider_horodatage(ligne.get("depart_horodatage"))
    if nettoyage_depart["erreur"] or not nettoyage_depart["valeur"]:
        return {"donnees": None, "erreur": nettoyage_depart["erreur"] or "depart_horodatage est obligatoire."}

    station_depart = str(ligne.get("station_depart", "")).strip()
    station_arrivee = str(ligne.get("station_arrivee", "")).strip() or None

    if station_depart not in ensemble_stations_valides:
        return {"donnees": None, "erreur": f"station_depart inconnue ou invalide : '{station_depart}'"}
    if station_arrivee and station_arrivee not in ensemble_stations_valides:
        return {"donnees": None, "erreur": f"station_arrivee inconnue ou invalide : '{station_arrivee}'"}

    try:
        duree_secondes = int(ligne.get("duree_secondes", 0))
        if duree_secondes <= 0:
            return {"donnees": None, "erreur": f"duree_secondes doit être > 0 (valeur: {ligne.get('duree_secondes')})"}
    except (ValueError, TypeError):
        return {"donnees": None, "erreur": f"duree_secondes invalide : '{ligne.get('duree_secondes')}'"}

    type_usager = str(ligne.get("type_usager", "")).strip().lower()
    if type_usager not in ("abonne", "occasionnel"):
        return {"donnees": None, "erreur": f"type_usager invalide : '{type_usager}'"}

    nettoyage_usager_ref = valider_expression_reguliere(ligne.get("usager_ref"), r"^U[0-9A-Fa-f]{8}$", "usager_ref", optionnel=True)
    if nettoyage_usager_ref["erreur"]:
        return {"donnees": None, "erreur": nettoyage_usager_ref["erreur"]}

    if type_usager == "occasionnel" and nettoyage_usager_ref["valeur"] is not None:
        return {"donnees": None, "erreur": "Un usager occasionnel ne doit pas avoir d'usager_ref."}

    return {
        "donnees": {
            "trajet_id": nettoyage_trajet_id["valeur"],
            "velo_id": nettoyage_velo_id["valeur"],
            "depart_horodatage": nettoyage_depart["valeur"],
            "station_depart": station_depart,
            "station_arrivee": station_arrivee,
            "duree_secondes": duree_secondes,
            "type_usager": type_usager,
            "usager_ref": nettoyage_usager_ref["valeur"],
        },
        "erreur": None
    }


def fiabiliser_incident(ligne, ensemble_stations_valides):
    """Valide et normalise une ligne de la table des incidents."""
    nettoyage_incident_id = valider_expression_reguliere(ligne.get("incident_id"), r"^I2026-[0-9]{4}$", "incident_id")
    if nettoyage_incident_id["erreur"]:
        return {"donnees": None, "erreur": nettoyage_incident_id["erreur"]}

    nettoyage_date_signalement = valider_horodatage(ligne.get("date_signalement"))
    if nettoyage_date_signalement["erreur"] or not nettoyage_date_signalement["valeur"]:
        return {"donnees": None, "erreur": nettoyage_date_signalement["erreur"] or "date_signalement est obligatoire."}

    cible = str(ligne.get("cible", "")).strip().lower()
    if cible not in ("velo", "station"):
        return {"donnees": None, "erreur": f"cible invalide : '{cible}'"}

    nettoyage_velo_id = valider_expression_reguliere(ligne.get("velo_id"), r"^V[0-9]{4}$", "velo_id", optionnel=True)
    if nettoyage_velo_id["erreur"]:
        return {"donnees": None, "erreur": nettoyage_velo_id["erreur"]}
    
    station_id = str(ligne.get("station_id", "")).strip() or None

    if cible == "velo" and (not nettoyage_velo_id["valeur"] or station_id):
        return {"donnees": None, "erreur": "Cible 'velo' implique velo_id renseigné et station_id vide."}
    if cible == "station" and (not station_id or nettoyage_velo_id["valeur"]):
        return {"donnees": None, "erreur": "Cible 'station' implique station_id renseigné et velo_id vide."}
    if station_id and station_id not in ensemble_stations_valides:
        return {"donnees": None, "erreur": f"station_id inconnu ou invalide : '{station_id}'"}

    statut = str(ligne.get("statut", "")).strip().lower()
    if statut not in ("ouvert", "en_cours", "resolu"):
        return {"donnees": None, "erreur": f"statut invalide : '{statut}'"}

    nettoyage_date_resolution = valider_horodatage(ligne.get("date_resolution"))
    if nettoyage_date_resolution["erreur"]:
        return {"donnees": None, "erreur": nettoyage_date_resolution["erreur"]}

    date_resolution = nettoyage_date_resolution["valeur"]
    date_signalement = nettoyage_date_signalement["valeur"]

    if statut == "resolu" and not date_resolution:
        return {"donnees": None, "erreur": "date_resolution obligatoire pour un incident résolu."}
    if statut != "resolu" and date_resolution:
        return {"donnees": None, "erreur": "date_resolution doit être vide si l'incident n'est pas résolu."}
    if date_resolution and date_resolution < date_signalement:
        return {"donnees": None, "erreur": "date_resolution ne peut pas être antérieure à date_signalement."}

    return {
        "donnees": {
            "incident_id": nettoyage_incident_id["valeur"],
            "date_signalement": date_signalement,
            "cible": cible,
            "velo_id": nettoyage_velo_id["valeur"],
            "station_id": station_id,
            "type_incident": str(ligne.get("type_incident", "")).strip(),
            "statut": statut,
            "date_resolution": date_resolution,
            "technicien": str(ligne.get("technicien", "")).strip() or None,
        },
        "erreur": None
    }