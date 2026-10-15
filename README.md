# VéloVille Hauts-de-France — L'application de gestion des vélos en libre-service de la ville (ver.1.0.0)

Bienvenue sur le dépôt de la plateforme de valorisation des données de **VéloVille**. Ce projet permet l'ingestion, la fiabilisation, l'exposition par API sécurisée et la restitution tabulaire des données d'exploitation des vélos en libre-service (stations, trajets, incidents).

---

## Prérequis

- **Python** : 3.10 ou supérieur
- **PostgreSQL** : 14 ou supérieur
- **Bash** / **Git**

---

## Installation pas à pas

### 1. Clonage du dépôt et création de l'environnement virtuel
```bash
git clone <url-du-depot-git>

cd veloville
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
### 2. Configuration des variables d'environnement

Copier le fichier `.env.exemple` en `.env` et renseigner les valeurs.
Le fichier .env ne doit JAMAIS être commité (voir `.gitignore`).

### 3. Initialisation de la base de données

1. Se connecter à PostgreSQL pour créer la base et le rôle applicatif :

```bash
SQL :

CREATE USER veloville WITH PASSWORD 'veloville';
CREATE DATABASE veloville OWNER veloville;
```

Se connecter à la base veloville puis éxécuter le code SQL du fichier : 
`ressources\squelette-git\sql\schema.sql`
Pour créer des comptes-tests :
`ressources\squelette-git\sql\comptes.sql`

2. Importation et fiabilisation des données

Pour lancer l'ingestion rejouable des données CSV (data/stations.csv, data/trajets.csv, data/incidents.csv) avec nettoyage et journalisation des éjections, lancer le code `ressources\squelette-git\scripts\importer.py`

### 4. Lancement des services

1. Lancer l'API Backend (FastAPI)
```Bash
uvicorn api.main:app --reload --port 8000
```
- Documentation Swagger interactive : ```http://localhost:8000/docs```

- Endpoint de santé : ```http://localhost:8000/sante```

2. Lancer l'interface utilisateur (Streamlit)
**Dans un autre terminal** :

```Bash
streamlit run front/app.py
```
Interface accessible sur : ```http://localhost:8501```

---

## Exécution des tests et couverture

Pour exécuter la suite complète de tests unitaires et d'intégration :

```Bash
pytest --cov=api --cov-report=term-missing
```
Couverture obtenue : 84% (exigence minimale : 60%).

---

## Choix écoresponsables & Écoconception

- Agrégations côté SGBD : Les indicateurs décisionnels sont calculés directement en SQL pour minimiser le transfert réseau et le volume mémoire.
- Consultation à la demande : Aucun mécanisme de rafraîchissement temps réel inutile.
- Pagination systématique : Bornage strict des réponses API pour éviter les surcharges de rendu.
- Mise en cache local : Données de référence peu volatiles (référentiel des stations) conservées en cache session côté front.

---

## Limites connues & Périmètre ver.1.0.0

- Pas d'interface Web de gestion des utilisateurs (création via SQL ou backend).
- Absence de visualisations graphiques (restitution tabulaire en V1, excepté 1 graphe d'indicateurs).
- Pas de gestion temps réel de la météo ni du rééquilibrage de flotte (prévus pour la V2).