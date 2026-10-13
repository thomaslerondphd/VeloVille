"""Import, fiabilisation et exportation des données CSV dans PostgreSQL.

Lit data/stations.csv, data/trajets.csv et data/incidents.csv,
applique les règles de fiabilisation (api/services/fiabilisation.py),
sauvegarde les fichiers nettoyés dans le dossier data,
et charge les lignes valides de façon idempotente en base.

Usage prévu : python scripts/importer.py [--dossier data]
"""

import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import dotenv
import datetime

# Résolution du problème d'import : ajout de la racine du projet au sys.path
CHEMIN_RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if CHEMIN_RACINE not in sys.path:
    sys.path.insert(0, CHEMIN_RACINE)

from api.services.fiabilisation import (
    fiabiliser_station,
    fiabiliser_trajet,
    fiabiliser_incident,
)

# Chargement des variables d'environnement
dotenv.load_config() if hasattr(dotenv, "load_config") else dotenv.load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/bloc2"
)

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    """Classe mère de tous les modèles."""
    pass


SessionLocal = sessionmaker(bind=engine, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def sauvegarder_csv_propres(dossier_data, nom_fichier_base, liste_donnees):
    """Exporte la liste des données nettoyées dans un nouveau CSV propre."""
    if not liste_donnees:
        return

    df_propre = pd.DataFrame(liste_donnees)
    nom_fichier_propre = f"{nom_fichier_base}_propres.csv"
    chemin_sortie = os.path.join(dossier_data, nom_fichier_propre)
    
    df_propre.to_csv(chemin_sortie, index=False, encoding="utf-8")
    print(f"CSV nettoyé créé : {chemin_sortie}")


def generer_rapport_readme(stats_import, chemin_readme="README.md"):
    """Met à jour le fichier README.md avec le bilan détaillé de l'importation."""
    date_exec = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    contenu_rapport = f"""

## Bilan de la dernière fiabilisation ({date_exec})

### 1. Synthèse par entité
| Entité | Lignes lues | Valides (Chargées) | Avertissements (Modifiées) | Rejets (Erreurs) |
| :--- | :---: | :---: | :---: | :---: |
| **Stations** | {stats_import['stations']['total']} | {stats_import['stations']['valides']} | {stats_import['stations']['avertissements_nb']} | {stats_import['stations']['rejets_nb']} |
| **Trajets** | {stats_import['trajets']['total']} | {stats_import['trajets']['valides']} | {stats_import['trajets']['avertissements_nb']} | {stats_import['trajets']['rejets_nb']} |
| **Incidents** | {stats_import['incidents']['total']} | {stats_import['incidents']['valides']} | {stats_import['incidents']['avertissements_nb']} | {stats_import['incidents']['rejets_nb']} |

### 2. Journal des rejets (Lignes exclues)
"""
    
    rejets_existants = False
    for entite, datas in stats_import.items():
        if datas["rejets"]:
            rejets_existants = True
            contenu_rapport += f"\n#### {entite.capitalize()}\n"
            for r in datas["rejets"]:
                contenu_rapport += f"- **Ligne {r['ligne']}** : {r['motif']}\n"
    
    if not rejets_existants:
        contenu_rapport += "\n*Aucune ligne rejetée lors du dernier import.*\n"

    contenu_rapport += "\n### 3. Journal des avertissements (Lignes conservées mais modifiées)\n"
    
    avertissements_existants = False
    for entite, datas in stats_import.items():
        if datas["avertissements"]:
            avertissements_existants = True
            contenu_rapport += f"\n#### {entite.capitalize()}\n"
            for a in datas["avertissements"]:
                contenu_rapport += f"- **Ligne {a['ligne']}** : {a['message']}\n"
                
    if not avertissements_existants:
        contenu_rapport += "\n*Aucun avertissement lors du dernier import.*\n"

    if os.path.exists(chemin_readme):
        with open(chemin_readme, "r", encoding="utf-8") as f:
            texte_existant = f.read()
        
        if "## Bilan de la dernière fiabilisation" in texte_existant:
            texte_existant = texte_existant.split("## Bilan de la dernière fiabilisation")[0]
            
        nouveau_texte = texte_existant.strip() + "\n" + contenu_rapport
    else:
        nouveau_texte = f"# Projet VéloVille\n{contenu_rapport}"

    with open(chemin_readme, "w", encoding="utf-8") as f:
        f.write(nouveau_texte)

    print(f"Rapport mis à jour dans {chemin_readme}")


def inserer_ou_mettre_a_jour(moteur, nom_table, liste_donnees, p_key):
    """Insère en base de manière idempotente (ON CONFLICT DO UPDATE)."""
    if not liste_donnees:
        return

    with moteur.begin() as connexion:
        for ligne in liste_donnees:
            liste_colonnes = list(ligne.keys())
            expressions_mise_a_jour = ", ".join(
                [f"{colonne} = EXCLUDED.{colonne}" for colonne in liste_colonnes if colonne != p_key]
            )
            
            requete_sql = f"""
                INSERT INTO {nom_table} ({', '.join(liste_colonnes)})
                VALUES ({', '.join([':' + colonne for colonne in liste_colonnes])})
                ON CONFLICT ({p_key}) DO UPDATE SET {expressions_mise_a_jour};
            """
            connexion.execute(text(requete_sql), ligne)


def charger_et_importer(dossier_data):
    """Lit les CSV, fiabilise, génère les CSV propres et fait l'import PostgreSQL."""
    
    stats_import = {
        "stations": {"total": 0, "valides": 0, "rejets_nb": 0, "avertissements_nb": 0, "rejets": [], "avertissements": []},
        "trajets": {"total": 0, "valides": 0, "rejets_nb": 0, "avertissements_nb": 0, "rejets": [], "avertissements": []},
        "incidents": {"total": 0, "valides": 0, "rejets_nb": 0, "avertissements_nb": 0, "rejets": [], "avertissements": []},
    }
    
    # 1. STATIONS
    fichier_stations = os.path.join(dossier_data, "stations.csv")
    if not os.path.exists(fichier_stations):
        print(f"Erreur : Fichier introuvable ({fichier_stations})")
        return

    tableau_stations = pd.read_csv(fichier_stations, dtype=str).fillna("")
    stats_import["stations"]["total"] = len(tableau_stations)
    stations_nettoyes = []
    identifiants_stations_nettoyes = set()

    for index_ligne, ligne in tableau_stations.iterrows():
        num_ligne = index_ligne + 2
        res = fiabiliser_station(ligne.to_dict())
        donnees_propres = res.get("donnees")
        erreur = res.get("erreur")
        avertissement = res.get("avertissement")

        if erreur:
            print(f"[REJET STATIONS] Ligne {num_ligne} : {erreur}")
            stats_import["stations"]["rejets_nb"] += 1
            stats_import["stations"]["rejets"].append({"ligne": num_ligne, "motif": erreur})
        else:
            if avertissement:
                print(f"[AVERTISSEMENT STATIONS] Ligne {num_ligne} : {avertissement}")
                stats_import["stations"]["avertissements_nb"] += 1
                stats_import["stations"]["avertissements"].append({"ligne": num_ligne, "message": avertissement})
            stations_nettoyes.append(donnees_propres)
            identifiants_stations_nettoyes.add(donnees_propres["station_id"])

    stats_import["stations"]["valides"] = len(stations_nettoyes)
    sauvegarder_csv_propres(dossier_data, "stations", stations_nettoyes)
    inserer_ou_mettre_a_jour(engine, "stations", stations_nettoyes, "station_id")
    print(f"-> Stations importées : {len(stations_nettoyes)} / {len(tableau_stations)}")

    # 2. TRAJETS
    fichier_trajets = os.path.join(dossier_data, "trajets.csv")
    if not os.path.exists(fichier_trajets):
        print(f"Erreur : Fichier introuvable ({fichier_trajets})")
        return

    tableau_trajets = pd.read_csv(fichier_trajets, dtype=str).fillna("")
    stats_import["trajets"]["total"] = len(tableau_trajets)
    trajets_nettoyes = []

    for index_ligne, ligne in tableau_trajets.iterrows():
        num_ligne = index_ligne + 2
        res = fiabiliser_trajet(ligne.to_dict(), identifiants_stations_nettoyes)
        donnees_propres = res.get("donnees")
        erreur = res.get("erreur")
        avertissement = res.get("avertissement")

        if erreur:
            stats_import["trajets"]["rejets_nb"] += 1
            stats_import["trajets"]["rejets"].append({"ligne": num_ligne, "motif": erreur})
            print(f"[REJET TRAJETS] Ligne {num_ligne} : {erreur}")
        else:
            if avertissement:
                stats_import["trajets"]["avertissements_nb"] += 1
                stats_import["trajets"]["avertissements"].append({"ligne": num_ligne, "message": avertissement})
                print(f"[AVERTISSEMENT TRAJETS] Ligne {num_ligne} : {avertissement}")
            trajets_nettoyes.append(donnees_propres)

    stats_import["trajets"]["valides"] = len(trajets_nettoyes)
    sauvegarder_csv_propres(dossier_data, "trajets", trajets_nettoyes)
    inserer_ou_mettre_a_jour(engine, "trajets", trajets_nettoyes, "trajet_id")
    print(f"-> Trajets importés : {len(trajets_nettoyes)} / {len(tableau_trajets)}")

    # 3. INCIDENTS
    fichier_incidents = os.path.join(dossier_data, "incidents.csv")
    if not os.path.exists(fichier_incidents):
        print(f"Erreur : Fichier introuvable ({fichier_incidents})")
        return

    tableau_incidents = pd.read_csv(fichier_incidents, dtype=str).fillna("")
    stats_import["incidents"]["total"] = len(tableau_incidents)
    incidents_nettoyes = []

    for index_ligne, ligne in tableau_incidents.iterrows():
        num_ligne = index_ligne + 2
        res = fiabiliser_incident(ligne.to_dict(), identifiants_stations_nettoyes)
        donnees_propres = res.get("donnees")
        erreur = res.get("erreur")
        avertissement = res.get("avertissement")

        if erreur:
            stats_import["incidents"]["rejets_nb"] += 1
            stats_import["incidents"]["rejets"].append({"ligne": num_ligne, "motif": erreur})
            print(f"[REJET INCIDENTS] Ligne {num_ligne} : {erreur}")
        else:
            if avertissement:
                stats_import["incidents"]["avertissements_nb"] += 1
                stats_import["incidents"]["avertissements"].append({"ligne": num_ligne, "message": avertissement})
                print(f"[AVERTISSEMENT INCIDENTS] Ligne {num_ligne} : {avertissement}")
            incidents_nettoyes.append(donnees_propres)

    stats_import["incidents"]["valides"] = len(incidents_nettoyes)
    sauvegarder_csv_propres(dossier_data, "incidents", incidents_nettoyes)
    inserer_ou_mettre_a_jour(engine, "incidents", incidents_nettoyes, "incident_id")
    print(f"-> Incidents importés : {len(incidents_nettoyes)} / {len(tableau_incidents)}")

    # Génération du rapport Markdown
    generer_rapport_readme(stats_import)


def main() -> None:
    """Détermine le dossier cible des fichiers CSV et lance l'importation."""
    dossier_cible = "data"
    if not os.path.exists(dossier_cible):
        dossier_cible = os.path.join("ressources", "squelette-git", "data")

    charger_et_importer(dossier_cible)


if __name__ == "__main__":
    main()