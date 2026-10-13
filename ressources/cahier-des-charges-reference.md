# Cahier des charges — Plateforme de valorisation des données VéloVille

Version de référence 1.0 — validée par la direction de VéloVille
Hauts-de-France le 25/09/2026. Périmètre : version 1 (V1) de la plateforme.

Ce document est la référence contractuelle pour le développement de la V1.
Il remplace, pour l'épreuve, toute version du cahier des charges produite au
bloc 1.

## 1. Contexte

VéloVille Hauts-de-France exploite un service de vélos en libre-service sur
la métropole lilloise : 120 stations réparties sur 9 communes, 1 800 vélos,
environ 9 000 trajets par jour. Le service est exploité pour le compte d'un
délégataire public, auquel VéloVille rend compte mensuellement de l'activité
et de la qualité de service.

Les données sont aujourd'hui produites par le système de billettique
(retraits et restitutions de vélos) et par l'outil de maintenance
(signalement et suivi des incidents). Elles sont exportées à la demande sous
forme de fichiers CSV, retraités à la main dans un tableur par l'équipe
d'exploitation.

## 2. Existant et limites

- Les exports ne sont pas fiabilisés : doublons, références erronées,
  formats hétérogènes selon l'opérateur de saisie. Chaque retraitement
  manuel recommence le nettoyage.
- Aucun référentiel commun : un trajet peut mentionner une station qui
  n'existe pas ou plus ; un incident peut rester sans suivi.
- Les indicateurs mensuels sont produits à la main, avec des écarts d'un
  mois sur l'autre selon la personne qui les calcule.
- Les fichiers circulent par courriel, sans contrôle d'accès ni traçabilité.

## 3. Objectifs de la V1

1. Disposer d'une base de données unique, fiable et documentée des
   stations, des trajets et des incidents.
2. Automatiser l'import et la fiabilisation des exports, avec un journal des
   données écartées.
3. Exposer les données et trois indicateurs par une API sécurisée, afin que
   d'autres outils puissent les consommer.
4. Offrir aux équipes une restitution simple, consultable depuis un poste de
   travail ou une tablette, sans compétence technique.
5. Distinguer ce que peut faire un exploitant (suivre et traiter les
   incidents) de ce que peut faire la direction (consulter).

## 4. Acteurs

| Acteur | Rôle applicatif | Besoins |
|---|---|---|
| Agent d'exploitation | `exploitant` | Consulter stations, trajets et incidents ; faire avancer le statut d'un incident ; suivre l'activité |
| Direction et délégataire | `direction` | Consulter les mêmes données et les indicateurs ; aucune modification |
| Administrateur technique | hors application | Déployer, sauvegarder, gérer les comptes par script SQL |

La V1 ne comporte pas d'interface de gestion des comptes : les comptes sont
créés par script. Un troisième rôle (administrateur) est prévu en V2.

## 5. Périmètre fonctionnel

### 5.1 Données prises en charge

- **Stations** : référentiel des 120 stations (identifiant, nom, commune,
  capacité, coordonnées, date de mise en service).
- **Trajets** : locations de vélos (vélo, horodatage de départ, station de
  départ, station d'arrivée, durée, type d'usager, pseudonyme d'abonné).
- **Incidents** : signalements de maintenance visant un vélo ou une
  station (date, type, statut, date de résolution, technicien).

Les données météo, l'état en temps réel des stations et les prévisions de
rééquilibrage sont **hors périmètre V1**.

### 5.2 Fonctions

| Réf. | Fonction | Rôles |
|---|---|---|
| F1 | Importer les trois exports CSV, appliquer les règles de gestion, journaliser les rejets, de manière rejouable | administrateur technique (script) |
| F2 | Consulter les stations, filtrer par commune, paginer | exploitant, direction |
| F3 | Consulter une station par son identifiant | exploitant, direction |
| F4 | Consulter les trajets, filtrer par période et par station, paginer | exploitant, direction |
| F5 | Consulter les incidents, filtrer par statut, paginer | exploitant, direction |
| F6 | Faire évoluer le statut d'un incident | exploitant |
| F7 | Indicateur « activité par jour » : nombre de trajets par jour sur une période | exploitant, direction |
| F8 | Indicateur « stations actives » : les stations ayant le plus de départs et d'arrivées | exploitant, direction |
| F9 | Indicateur « incidents par statut » : répartition des incidents et délai moyen de résolution | exploitant, direction |
| F10 | S'authentifier par identifiant et mot de passe ; obtenir un jeton de session | tous |

### 5.3 Restitution

Un front web de restitution, en quatre écrans : connexion, stations,
incidents, indicateurs. La restitution est **tabulaire** (tableaux et
valeurs clés) ; la V1 ne comporte pas de graphique. Les écrans sont décrits
dans `maquettes-ecrans.md`.

## 6. Règles de gestion

| Réf. | Règle |
|---|---|
| RG1 | Une station est identifiée de façon unique par `station_id`. Sa capacité est un entier strictement positif. |
| RG2 | Un trajet relie deux stations du référentiel : la station de départ est obligatoire et doit exister ; la station d'arrivée, lorsqu'elle est renseignée, doit exister. |
| RG3 | La station d'arrivée d'un trajet peut être inconnue (vélo non restitué au moment de l'export). Le trajet est conservé ; il ne compte pas comme arrivée pour aucune station. |
| RG4 | La durée d'un trajet est un entier strictement positif, exprimé en secondes. |
| RG5 | Un trajet d'abonné porte un pseudonyme d'usager (`usager_ref`) ; un trajet d'usager occasionnel n'en porte pas. Aucune donnée directement identifiante n'est conservée. |
| RG6 | Un incident vise soit un vélo, soit une station, jamais les deux ni aucun : `cible` détermine laquelle des deux références est renseignée. Une station visée doit exister dans le référentiel. |
| RG7 | Un incident est dans l'un des trois statuts `ouvert`, `en_cours`, `resolu`. Les transitions autorisées sont `ouvert -> en_cours`, `ouvert -> resolu` et `en_cours -> resolu`. Un incident résolu n'évolue plus. |
| RG8 | La date de résolution est renseignée si et seulement si l'incident est résolu, et elle est postérieure ou égale à la date de signalement. Le nom du technicien est attendu dès la prise en charge ; son absence est signalée mais n'empêche pas l'enregistrement. |

Toute donnée source violant RG1, RG2, RG4, RG6, RG7 ou la cohérence de dates
de RG8 après normalisation est écartée de l'import et journalisée avec son
motif. Une valeur dont seule la forme est incorrecte (casse, format de date)
est normalisée et journalisée en avertissement.

## 7. Exigences non fonctionnelles

### 7.1 Performance et volumétrie

- Jeu de données V1 : 120 stations, un extrait de 2 000 trajets environ,
  180 incidents. Cible à 12 mois : 3 millions de trajets.
- Toute consultation paginée répond en moins de 2 secondes sur le jeu V1 ;
  les listes sont paginées côté serveur avec une taille de page bornée.
- Les indicateurs sont calculés par agrégation en base de données, pas en
  mémoire côté application.

### 7.2 Sécurité

- Accès à l'API soumis à authentification par jeton signé à durée limitée.
- Mots de passe stockés hachés avec un algorithme adapté (bcrypt).
- Droits distincts par rôle ; la modification d'un incident est réservée à
  l'exploitant.
- Aucun secret (mot de passe de base, clé de signature) dans le code source
  ni dans le dépôt : configuration par variables d'environnement.
- Les refus d'accès renvoient des codes HTTP explicites (401, 403) et des
  messages ne révélant pas d'information interne.

### 7.3 Protection des données personnelles (RGPD)

- Les trajets sont des données potentiellement ré-identifiantes. La V1 ne
  conserve que `usager_ref`, pseudonyme produit par la billettique ; aucune
  table d'abonnés n'est importée.
- `usager_ref` n'est pas affiché dans les écrans de restitution destinés à
  la direction ; il peut l'être pour l'exploitant à des fins de support.
- Durée de conservation des trajets détaillés : 13 mois ; une purge
  automatisée est prévue (V1 : script ; V2 : planification).
- Le registre des traitements et la mention d'information aux usagers sont
  tenus par VéloVille, hors périmètre applicatif.

### 7.4 Accessibilité

- Chaque champ de saisie, bouton et tableau porte un libellé explicite.
- Les messages d'état (chargement, absence de résultat, erreur) sont
  textuels et en français.
- Aucune information n'est portée uniquement par la couleur.
- Les écrans restent lisibles sur une tablette (largeur 768 px) : pas de
  défilement horizontal imposé en dehors des tableaux.

### 7.5 Écoconception

- Pas de rafraîchissement automatique ni de temps réel : les données sont
  chargées à la demande.
- Pagination systématique ; taille de page par défaut raisonnable.
- Mise en cache côté front des données de référence peu volatiles
  (stations).
- Agrégations en SQL ; pas de chargement de tables entières côté client.
- Dépendances limitées au nécessaire.

### 7.6 Exploitabilité et maintenance

- Import rejouable sans intervention manuelle.
- Sauvegarde de la base par script horodaté ; procédure de restauration
  documentée.
- Journal des versions (CHANGELOG) et historique de versioning lisible.
- Procédure de déploiement reproductible sur un poste vierge.

## 8. Contraintes

- Équipe de maintenance VéloVille : 2 développeurs, compétences Python et
  SQL. Toute la solution est donc en **Python** et **SQL**.
- Base de données : **PostgreSQL** (déjà exploité par VéloVille pour la
  billettique).
- Hébergement V1 : un serveur interne ; l'API et le front tournent sur la
  même machine. Le passage en production hébergée est hors périmètre V1.
- Budget V1 : enveloppe de développement forfaitaire ; livraison attendue
  en octobre 2026 pour une mise en recette interne.
- Comptes de recette fournis par VéloVille : un compte exploitant et un
  compte direction.

## 9. Livrables attendus du développeur

1. Le dépôt de code versionné, avec son historique.
2. Le schéma de données et son script de création.
3. Le script d'import et de fiabilisation, avec journal des rejets.
4. L'API et le front, déployables selon une procédure documentée.
5. Les tests automatisés et le taux de couverture des modules métier
   (minimum 60 %).
6. Les résultats de la recette menée sur le plan fourni par VéloVille, les
   fiches d'anomalie et les corrections.
7. La matrice des rôles et des droits.
8. Le script de sauvegarde et la procédure de restauration.
9. La documentation technique et fonctionnelle, le journal des versions.

## 10. Glossaire

| Terme | Définition |
|---|---|
| Station | Point d'attache de vélos, identifié et géolocalisé |
| Trajet | Location d'un vélo entre un retrait et une restitution |
| Incident | Signalement de maintenance portant sur un vélo ou une station |
| Exploitant | Agent de VéloVille chargé du terrain et de la maintenance |
| Direction | Encadrement de VéloVille et représentants du délégataire |
| Délégataire | Collectivité pour le compte de laquelle le service est exploité |
| Pseudonyme | Identifiant indirect ne permettant pas de retrouver la personne sans information complémentaire |
