-- Schéma de la base veloville (PostgreSQL 14+).
-- À compléter en respectant le contrat du sujet (types, clés, contraintes).
-- Le script doit être rejouable : prévoir les DROP ... IF EXISTS ou
-- CREATE TABLE IF NOT EXISTS.

-- ---------------------------------------------------------------
-- 0. Initialisation des tables
-- ---------------------------------------------------------------

DROP TABLE IF EXISTS stations ;
DROP TABLE IF EXISTS trajets ;
DROP TABLE IF EXISTS incidents ;
DROP TABLE IF EXISTS utilisateurs ;

-- ---------------------------------------------------------------
-- 1. Table stations
-- ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS stations (
    station_id VARCHAR(4) PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    commune VARCHAR(50) NOT NULL,
    capacite INTEGER NOT NULL,
    latitude NUMERIC(7, 5) NOT NULL,
    longitude NUMERIC(6, 5) NOT NULL,
    date_mise_en_service DATE NOT NULL,

-- Contrainte sur le format de l'identifiant (S + 3 chiffres)
	CONSTRAINT chk_station_id CHECK (station_id ~ '^S[0-9]{3}$'),
    
-- Contrainte sur la capacité (> 0)
	CONSTRAINT chk_capacite CHECK (capacite > 0)
	);

-- ---------------------------------------------------------------
-- 2. Table trajets
-- ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS trajets (
    trajet_id VARCHAR(7) PRIMARY KEY,
    velo_id VARCHAR(5) NOT NULL,
    depart_horodatage TIMESTAMP NOT NULL,
    station_depart VARCHAR(4) NOT NULL,
    station_arrivee VARCHAR(4),
    duree_secondes INTEGER NOT NULL,
    type_usager VARCHAR(20) NOT NULL,
    usager_ref VARCHAR(9),

    -- Clés étrangères vers la table stations
    CONSTRAINT fk_station_depart FOREIGN KEY (station_depart) REFERENCES stations(station_id),
    CONSTRAINT fk_station_arrivee FOREIGN KEY (station_arrivee) REFERENCES stations(station_id),

    -- Validation du format des identifiants (Regex)
    CONSTRAINT chk_trajet_id CHECK (trajet_id ~ '^T[0-9]{6}$'),
    CONSTRAINT chk_velo_id CHECK (velo_id ~ '^V[0-9]{4}$'),
    CONSTRAINT chk_usager_ref CHECK (usager_ref IS NULL OR usager_ref ~ '^U[0-9A-Fa-f]{8}$'),

    -- Validation des valeurs
    CONSTRAINT chk_duree CHECK (duree_secondes > 0),
    CONSTRAINT chk_type_usager CHECK (type_usager IN ('abonne', 'occasionnel')),

    -- Regle métier : usager_ref doit être renseigné UNIQUEMENT pour les abonnés
    CONSTRAINT chk_usager_ref_abonne CHECK (
        (type_usager = 'occasionnel' AND usager_ref IS NULL) OR
        (type_usager = 'abonne')
    )
);

-- ---------------------------------------------------------------
-- 3. Table incident
-- ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS incidents (
    incident_id VARCHAR(10) PRIMARY KEY,
    date_signalement TIMESTAMP NOT NULL,
    cible VARCHAR(10) NOT NULL,
    velo_id VARCHAR(5),
    station_id VARCHAR(4),
    type_incident VARCHAR(50) NOT NULL,
    statut VARCHAR(10) NOT NULL,
    date_resolution TIMESTAMP,
    technicien VARCHAR(100),

    -- Clé étrangère vers la table stations
    CONSTRAINT fk_incidents_station FOREIGN KEY (station_id) REFERENCES stations(station_id),

    -- Validation du format de l'ID incident (I2026- + 4 chiffres)
    CONSTRAINT chk_incident_id CHECK (incident_id ~ '^I2026-[0-9]{4}$'),

    -- Validation du format du velo_id
    CONSTRAINT chk_incidents_velo_id CHECK (velo_id IS NULL OR velo_id ~ '^V[0-9]{4}$'),

    -- Validation du type de cible
    CONSTRAINT chk_cible CHECK (cible IN ('velo', 'station')),

    -- Règle métier : velo_id renseigné ssi cible == 'velo'
    CONSTRAINT chk_cible_velo CHECK (
        (cible = 'velo' AND velo_id IS NOT NULL AND station_id IS NULL) OR
        (cible = 'station' AND station_id IS NOT NULL AND velo_id IS NULL)
    ),

    -- Catégories d'incidents
    CONSTRAINT chk_type_incident CHECK (
        type_incident IN (
            'vandalisme',
            'selle abimee',
            'eclairage HS',
            'chaine deraillee',
            'ecran borne illisible',
            'pneu creve',
            'frein defectueux',
            'borne hors service'
        )
    ),

    -- Catégories de statut
    CONSTRAINT chk_statut CHECK (statut IN ('ouvert', 'en_cours', 'resolu')),

    -- Règle métier : date_resolution renseignée ssi statut == 'resolu'
    CONSTRAINT chk_date_resolution_statut CHECK (
        (statut = 'resolu' AND date_resolution IS NOT NULL) OR
        (statut != 'resolu' AND date_resolution IS NULL)
    ),

    -- Règle métier : date_resolution >= date_signalement
    CONSTRAINT chk_date_resolution_coherence CHECK (
        date_resolution IS NULL OR date_resolution >= date_signalement
    )
);

-- ---------------------------------------------------------------
-- 4. Table utilisateur
-- ---------------------------------------------------------------

CREATE TABLE IF NOT EXISTS utilisateurs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,

    -- Validation des rôles autorisés dans l'application
    CONSTRAINT chk_role CHECK (role IN ('direction', 'exploitant'))
);    

-- ---------------------------------------------------------------
-- 5. Index utiles aux filtres et aux indicateurs
-- ---------------------------------------------------------------

-- Indexes pour accélérer les jointures et requêtes courantes sur la table stations
CREATE INDEX IF NOT EXISTS idx_trajets_station_depart ON trajets(station_depart);
CREATE INDEX IF NOT EXISTS idx_trajets_station_arrivee ON trajets(station_arrivee);
CREATE INDEX IF NOT EXISTS idx_trajets_depart_horodatage ON trajets(depart_horodatage);

-- Indexes pour accélérer les recherches et filtres sur la table incidents
CREATE INDEX IF NOT EXISTS idx_incidents_station_id ON incidents(station_id);
CREATE INDEX IF NOT EXISTS idx_incidents_velo_id ON incidents(velo_id);
CREATE INDEX IF NOT EXISTS idx_incidents_statut ON incidents(statut);
CREATE INDEX IF NOT EXISTS idx_incidents_date_signalement ON incidents(date_signalement);

-- Indexes pour accélérer les vérifications d'authentification par username sur la table utilisateurs
CREATE INDEX IF NOT EXISTS idx_utilisateurs_username ON utilisateurs(username);
