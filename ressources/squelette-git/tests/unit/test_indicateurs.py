"""Tests des fonctions de calcul des indicateurs.

À compléter : vérifier les agrégats sur un jeu de données connu.
"""

def test_lister_stations_exploitant(
    client,
    exploitant_token,
):
    """L'exploitant possède le rôle attendu : 200."""

    response = client.get(
        "/stations",
        headers={
            "Authorization": f"Bearer {exploitant_token}"
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data["resultats"]) == 3



def test_lister_stations_sans_connexion_leve_erreur(client):
    r = client.get("/stations")
    assert r.status_code == 401
    
def rechercher_une_station(client, exploitant_token):
    response = client.get(
            "/stations/S001",
            headers={
                "Authorization": f"Bearer {exploitant_token}"
            },
        )
    assert response.nom == "Lille - Gare"
    assert response.commune == "Lille"
    assert response.capacite == 15
    
def rechercher_une_station_non_existante_leve_erreur(client, exploitant_token):
    response = client.get(
            "/stations/S999",
            headers={
                "Authorization": f"Bearer {exploitant_token}"
            },
        )
    assert r.status_code == 404


def test_lister_incidents_exploitant(
    client,
    exploitant_token,
):
    """L'exploitant possède le rôle attendu : 200."""

    response = client.get(
        "/incidents",
        headers={
            "Authorization": f"Bearer {exploitant_token}"
        },
    )

    data = response.json()
    assert response.status_code == 200
    assert len(data["resultats"]) == 2
    
def test_lister_incidents_sans_connexion_leve_erreur(
    client,
):
    """sans connexion  : erreur 401."""

    response = client.get(
        "/incidents",
    )

    assert response.status_code == 401

def test_maj_incident_exploitant(
    client,
    exploitant_token,
):
    """L'exploitant peut mettre à jour le statut d'un incident : 200."""

    response = client.put(
        "/incidents/I2026-0001/statut",
        json={"statut": "resolu"},
        headers={
            "Authorization": f"Bearer {exploitant_token}"
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["incident_id"] == "I2026-0001"
    assert data["statut"] == "resolu"
    assert data["cible"] == "station"

def test_maj_incident_exploitant_mauvaise_transition(
    client,
    exploitant_token,
):

    response = client.put(
        "/incidents/I2026-0001/statut",
        json={"statut": "ouvert"},
        headers={
            "Authorization": f"Bearer {exploitant_token}"
        },
    )

    assert response.status_code == 422

def test_maj_incident_exploitant_sans_authentification_leve_erreur(
    client,
):

    response = client.put(
        "/incidents/I2026-0001/statut",
        json={"statut": "ouvert"},
    )

    assert response.status_code == 401
    
def test_lister_trajets_sans_authentification_leve_erreur(client):
    """Accès refusé sans jeton d'authentification : 401."""
    response = client.get("/trajets")
    assert response.status_code == 401
    
def test_lister_trajets_exploitant(client,
                                   exploitant_token,
                                   ):
    """L'exploitant accède à la liste des trajets : 200."""
    response = client.get(
        "/trajets",
        headers={"Authorization": f"Bearer {exploitant_token}"},
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data["resultats"]) == 3


def test_activite_par_jour_direction(client,
                                     direction_token,
                                     ):
    """Accès autorisé pour le rôle direction : 200 et structure valide."""
    response = client.get(
        "/indicateurs/activite-par-jour",
        headers={"Authorization": f"Bearer {direction_token}"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["donnees"][0]["jour"] == "2026-06-01"
    assert data["donnees"][0]["nb_trajets"] == 3



def test_stations_actives_defaut(client, direction_token):
    """Récupération du top des stations actives avec paramètres par défaut."""
    response = client.get(
        "/indicateurs/stations-actives",
        headers={"Authorization": f"Bearer {direction_token}"},
    )

    data = response.json()
    assert response.status_code == 200
    assert data["donnees"][0]["station_id"] == "S001"
    assert data["donnees"][0]["nb_departs"] == 1


def test_stations_actives_tri_invalide_leve_erreur(client, direction_token):
    """Un critère de tri invalide doit renvoyer une erreur 422."""
    response = client.get(
        "/indicateurs/stations-actives?tri=a",
        headers={"Authorization": f"Bearer {direction_token}"},
    )
    assert response.status_code == 422


def test_incidents_par_statut(client, direction_token):
    """Répartition des incidents et délai moyen de résolution."""
    response = client.get(
        "/indicateurs/incidents-par-statut",
        headers={"Authorization": f"Bearer {direction_token}"},
    )

    data = response.json()
    incidents_en_cours = next((item for item in data["donnees"] if item["statut"] == "en_cours"), {"nb_incidents": 0})
    incidents_ouverts = next((item for item in data["donnees"] if item["statut"] == "ouvert"), {"nb_incidents": 0})
    incidents_resolus = next((item for item in data["donnees"] if item["statut"] == "resolu"), {"nb_incidents": 0})
    
    assert response.status_code == 200
    assert incidents_en_cours["nb_incidents"] == 1
    assert incidents_ouverts["nb_incidents"] == 0
    assert incidents_resolus["nb_incidents"] == 1
 
