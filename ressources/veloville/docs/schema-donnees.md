# Schéma de données

## 1. Structure MLD (Textuel)

- **stations** (<u>station_id</u>, nom, commune, capacite, latitude, longitude, date_mise_en_service)
- **trajets** (<u>trajet_id</u>, velo_id, depart_horodatage, #station_depart, #station_arrivee, duree_secondes, type_usager, usager_ref)
- **incidents** (<u>incident_id</u>, date_signalement, cible, velo_id, #station_id, type_incident, statut, date_resolution, technicien)
- **utilisateurs** (<u>utilisateur_id</u>, identifiant, mot_de_passe_hash, role, date_creation)

---

## 2. Description des Tables et Contraintes

### Table `stations`
| Colonne | Type | Contrainte | Description |
| :--- | :--- | :--- | :--- |
| `station_id` | `VARCHAR(4)` | `PRIMARY KEY`, `CHECK (~ '^S[0-9]{3}$')` | Identifiant station (ex: S001) |
| `nom` | `VARCHAR(50)` | `NOT NULL` | Nom de la station |
| `commune` | `VARCHAR(50)` | `NOT NULL` | Commune |
| `capacite` | `INTEGER` | `NOT NULL`, `CHECK (> 0)` | Nombre de vélos maximum sur la station |
| `latitude` | `NUMERIC(7,5)`| `NOT NULL` | Coordonnée latitude |
| `longitude` | `NUMERIC(6,5)`| `NOT NULL` | Coordonnée longitude |
| `date_mise_en_service` | `DATE` | `NOT NULL` | Date de mise en service |

### Table `trajets`
| Colonne | Type | Contrainte | Description |
| :--- | :--- | :--- | :--- |
| `trajet_id` | `VARCHAR(7)` | `PRIMARY KEY`, `CHECK (~ '^T[0-9]{6}$')` | Identifiant trajet (ex: T000001) |
| `velo_id` | `VARCHAR(5)` | `NOT NULL`, `CHECK (~ '^V[0-9]{4}$')` | Identifiant du vélo (ex: V0001) |
| `depart_horodatage` | `TIMESTAMP` | `NOT NULL` | Horodatage de début de trajet |
| `station_depart` | `VARCHAR(4)` | `NOT NULL`, `FOREIGN KEY` | Réf station départ (`stations.station_id`) |
| `station_arrivee` | `VARCHAR(4)` | `FOREIGN KEY` | Réf station arrivée (`stations.station_id`) |
| `duree_secondes` | `INTEGER` | `NOT NULL`, `CHECK (> 0)` | Durée du trajet |
| `type_usager` | `VARCHAR(20)` | `CHECK (IN ('abonne', 'occasionnel'))` | Profil de l'usager |
| `usager_ref` | `VARCHAR(9)` |  `CHECK (~ '^U[0-9A-Fa-f]{8}$')` | Réf anonymisée de l'abonné |

### Table `incidents`
| Colonne | Type | Contrainte | Description |
| :--- | :--- | :--- | :--- |
| `incident_id` | `VARCHAR(10)`| `PRIMARY KEY`, `CHECK (~ '^I2026-[0-9]{4}$')` | Identifiant incident |
| `date_signalement` | `TIMESTAMP` | `NOT NULL` | Date et heure d'entrée de l'incident |
| `cible` | `VARCHAR(10)` | `CHECK (IN ('velo', 'station'))` | Élément concerné (station ou vélo) |
| `velo_id` | `VARCHAR(5)` |  `CHECK (~ '^V[0-9]{4}$')` | Réf vélo si cible == velo |
| `station_id` | `VARCHAR(4)` |  `FOREIGN KEY` | Réf station si cible == station |
| `type_incident` | `VARCHAR(50)` | `NOT NULL` | Type de l'incident |
| `statut` | `VARCHAR(10)` | `CHECK (IN ('ouvert', 'en_cours', 'resolu'))` | État d'avancement |
| `date_resolution` | `TIMESTAMP` |  | Date de clôture |
| `technicien` | `VARCHAR(100)`|  | Nom du technicien |

---

## 3. Matrice de prise en charge des Règles de Gestion (RG1 à RG8)

| RG | Intitulé court | Portée par le Schéma SQL | Portée par le Script d'Import (`importer.py`) |
| :--- | :--- | :--- | :--- |
| **RG1** | Unicité station & capacité > 0 | `PRIMARY KEY(station_id)`, `CHECK (capacite > 0)` | Filtrage regex `^S[0-9]{3}$` et rejets des entiers négatifs. |
| **RG2** | Stations départ/arrivée obligatoires ou existantes | `FK fk_station_depart` & `fk_station_arrivee` vers `stations` | Vérification de l'existence de la station dans le référentiel avant insertion. |
| **RG3** | Station d'arrivée inconnue autorisée | Colonne `station_arrivee` nullable | Conservation des trajets sans station d'arrivée (non comptabilisés aux arrivées). |
| **RG4** | Durée trajet strictement positive | `CHECK (duree_secondes > 0)` | Rejet des lignes avec durée <= 0 secondes avec journalisation. |
| **RG5** | Pseudonyme usager (RGPD) | `CHECK (type_usager = 'occasionnel' AND usager_ref IS NULL) OR ...` | Normalisation et suppression de `usager_ref` pour les usagers occasionnels. |
| **RG6** | Exclusivité Cible Vélo / Station | `CHECK ((cible='velo' AND velo_id IS NOT NULL AND station_id IS NULL) OR ...)` | Éjection des incidents ayant à la fois un vélo et une station renseignés (ou aucun). |
| **RG7** | Cycles de statuts d'incidents | `CHECK (statut IN ('ouvert', 'en_cours', 'resolu'))` | Validation applicative des transitions (ex: interdiction de repasser de `resolu` à `ouvert`). |
| **RG8** | Coherence des dates de résolution | `CHECK (date_resolution IS NULL OR date_resolution >= date_signalement)` | Filtrage des dates de résolution antérieures au signalement ; alerte si technicien absent. |