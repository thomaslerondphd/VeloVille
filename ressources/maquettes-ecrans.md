# Maquettes des écrans — front VéloVille V1 (Streamlit)

Quatre écrans, restitution tabulaire uniquement. Les maquettes ci-dessous
sont textuelles : elles fixent les champs, filtres, tableaux et métriques
attendus, pas la mise en forme. La barre latérale de navigation est celle
de Streamlit (pages `1_Stations`, `2_Incidents`, `3_Indicateurs`).

Conventions communes :

- Le nom de l'utilisateur connecté et son rôle sont affichés dans la barre
  latérale, avec un bouton « Se déconnecter ».
- Un écran ouvert sans jeton affiche « Veuillez vous connecter » et un lien
  vers la page de connexion ; il n'appelle pas l'API.
- Trois états par écran : **chargement** (`st.spinner` « Chargement... »),
  **vide** (`st.info` « Aucun résultat pour ces critères. »), **erreur**
  (`st.error` avec le message de `ErreurApi`, par exemple « L'API est
  injoignable. Vérifiez qu'elle est démarrée. »).
- Les tableaux sont rendus avec `st.dataframe` ; les en-têtes de colonnes
  sont en français lisible (« Station de départ » plutôt que
  `station_depart`).
- Aucune information portée uniquement par la couleur ; aucun graphique.

## Écran 1 — Connexion (`front/app.py`)

```
+--------------------------------------------------------------------+
|  VéloVille — Plateforme de restitution                             |
+--------------------------------------------------------------------+
|                                                                    |
|  Connexion                                                         |
|                                                                    |
|  Identifiant      [ exploitant01                        ]          |
|  Mot de passe     [ ************                        ]          |
|                                                                    |
|  [ Se connecter ]                                                  |
|                                                                    |
|  (après succès)                                                    |
|  Connecté en tant que exploitant01 (rôle : exploitant).            |
|  Utilisez le menu latéral pour accéder aux écrans.                 |
|                                                                    |
|  (après échec)                                                     |
|  Identifiant ou mot de passe incorrect.                            |
|                                                                    |
|  (API arrêtée)                                                     |
|  L'API est injoignable. Vérifiez qu'elle est démarrée.             |
+--------------------------------------------------------------------+
```

Comportement :

- Formulaire `st.form` ; le mot de passe est saisi en champ masqué.
- Succès : `access_token` et `role` stockés dans `st.session_state`, ainsi
  que l'identifiant saisi. Le jeton n'est jamais affiché.
- Échec 401 : message « Identifiant ou mot de passe incorrect. ».
- Si l'utilisateur est déjà connecté, le formulaire est remplacé par le
  message de connexion et le bouton « Se déconnecter ».

## Écran 2 — Stations (`front/pages/1_Stations.py`)

```
+--------------------------------------------------------------------+
|  Stations                                                          |
+--------------------------------------------------------------------+
|  Commune   [ Toutes            v ]   Taille de page [ 20  v ]      |
|  Page      [ 1 ] (-) (+)              120 stations au total        |
+--------------------------------------------------------------------+
|  Identifiant | Nom                    | Commune | Capacité | Mise   |
|              |                        |         |          | en     |
|              |                        |         |          | service|
|  S001        | Lille - Gare           | Lille   |   15     | 2023-  |
|  S002        | Lille - Mairie         | Lille   |   30     | 2021-  |
|  ...         | ...                    | ...     |   ...    | ...    |
+--------------------------------------------------------------------+
|  Page 1 sur 6                                                      |
+--------------------------------------------------------------------+
```

Comportement :

- Liste déroulante « Commune » alimentée par les communes distinctes des
  stations (chargement avec `st.cache_data`, durée de vie de l'ordre de
  l'heure) ; valeur « Toutes » = pas de filtre.
- Taille de page au choix parmi 10, 20, 50 ; page saisie ou incrémentée.
- Appel `GET /stations?commune=&page=&taille_page=` ; `total` affiché ;
  nombre de pages calculé à partir de `total` et `taille_page`.
- Colonnes affichées : identifiant, nom, commune, capacité, date de mise en
  service. Latitude et longitude facultatives.

## Écran 3 — Incidents (`front/pages/2_Incidents.py`)

```
+--------------------------------------------------------------------+
|  Incidents                                                         |
+--------------------------------------------------------------------+
|  Statut  [ Tous      v ]   Taille de page [ 20 v ]   Page [ 1 ]    |
|  180 incidents au total                                            |
+--------------------------------------------------------------------+
|  Identifiant | Signalé le       | Cible   | Vélo  | Station | Type |
|              |                  |         |       |         |      |
|  I2026-0180  | 2026-08-30 18:00 | station |       | S042    | ...  |
|  I2026-0177  | 2026-08-30 11:00 | velo    | V0210 |         | ...  |
|  ...                                                               |
|  (colonnes suivantes : Statut | Résolu le | Technicien)            |
+--------------------------------------------------------------------+
|  Changer le statut d'un incident          (rôle exploitant)        |
|  Incident        [ I2026-0180          v ]                         |
|  Nouveau statut  [ en_cours            v ]                         |
|  [ Appliquer ]                                                     |
|                                                                    |
|  Statut de l'incident I2026-0180 mis à jour : en_cours.            |
|  (ou) Transition de statut non autorisée.                          |
|  (ou, rôle direction) Vous n'avez pas le droit de modifier un      |
|  incident.                                                         |
+--------------------------------------------------------------------+
```

Comportement :

- Filtre « Statut » : Tous, ouvert, en_cours, resolu. Pagination comme
  l'écran Stations.
- Appel `GET /incidents?statut=&page=&taille_page=`.
- Section « Changer le statut d'un incident » : affichée seulement si le
  rôle en session est `exploitant`. Pour le rôle direction, elle est
  remplacée par la phrase « La modification des incidents est réservée aux
  exploitants. » (le front n'appelle pas le PUT). Si l'API renvoie
  néanmoins 403, le message « Vous n'avez pas le droit de modifier un
  incident. » est affiché.
- Liste des incidents de la page courante ; nouveau statut parmi `en_cours`
  et `resolu`. Appel `PUT /incidents/{incident_id}/statut`.
- Succès : message de confirmation et rechargement du tableau. Erreur 422 :
  message « Transition de statut non autorisée. ». Erreur 404 : « Incident
  introuvable. ».

## Écran 4 — Indicateurs (`front/pages/3_Indicateurs.py`)

```
+--------------------------------------------------------------------+
|  Indicateurs                                                       |
+--------------------------------------------------------------------+
|  Période : du [ 2026-08-24 ] au [ 2026-08-30 ]   Stations [ 10 ]   |
|  [ Actualiser ]                                                    |
+--------------------------------------------------------------------+
|  Trajets sur la période   | Stations actives     | Délai moyen de  |
|  2 0xx                    | 10                   | résolution (h)  |
|                           |                      | xx,x            |
+--------------------------------------------------------------------+
|  Activité par jour                                                 |
|  Jour        | Nombre de trajets                                   |
|  2026-08-24  | 3xx                                                 |
|  2026-08-25  | 3xx                                                 |
|  ...                                                               |
+--------------------------------------------------------------------+
|  Stations les plus actives                                         |
|  Identifiant | Nom              | Départs | Arrivées | Total       |
|  S0xx        | ...              |   xx    |   xx     |  xx         |
|  ...                                                               |
+--------------------------------------------------------------------+
|  Incidents par statut                                              |
|  Statut    | Nombre d'incidents                                    |
|  ouvert    | xx                                                    |
|  en_cours  | xx                                                    |
|  resolu    | xx                                                    |
+--------------------------------------------------------------------+
```

Comportement :

- Sélecteurs de dates (`st.date_input`) pour la période, valeurs par défaut
  couvrant la semaine fournie ; nombre de stations (`st.number_input`,
  1 à 50, défaut 10).
- Trois appels : `GET /indicateurs/activite-par-jour?date_debut=&date_fin=`,
  `GET /indicateurs/stations-actives?limite=`,
  `GET /indicateurs/incidents-par-statut`.
- Trois `st.metric` : « Trajets sur la période » (somme des `nb_trajets`),
  « Stations actives » (nombre d'éléments retournés), « Délai moyen de
  résolution (h) » (`delai_moyen_resolution_heures`, ou « n. d. » si
  `null`).
- Trois tableaux, dans l'ordre de la maquette. Colonne « Total » du second
  tableau calculée côté front (`nb_departs + nb_arrivees`).
- Aucun graphique.

## Barre latérale (toutes les pages)

```
+----------------------------+
|  app                       |
|  1 Stations                |
|  2 Incidents               |
|  3 Indicateurs             |
|                            |
|  Connecté : exploitant01   |
|  Rôle : exploitant         |
|  [ Se déconnecter ]        |
+----------------------------+
```

« Se déconnecter » vide `st.session_state` (jeton, rôle, identifiant) et
renvoie vers la page de connexion.
