# Procès-verbal de recette — VéloVille V1 <1.0.0>

## 1. Identification
- Application `VéloVille`
- Version testée : `ver.1.0.0`, commit `9b21e0d`
- date : 15/10/2026
- Environnement : 
    - poste Hermitage-3-3 ; 
    - Base SQL : `PostgreSQL\18\pgAdmin 4`
    - python : Python 3.14.7 , VS code 1.141.0
- Particiapants : Thomas Lerond
- rôle : Testeur

## 2. Périmètre recetté

- Testés : REC-01, REC-02, REC-03, REC-04, REC-05, REC-06, REC-07, REC-08, REC-09, REC-10 (en partie, cf partie Non testés)
- Non testés : REC-10 filtrage des incidents par statut : L'affichage Frontend ne prévoit pas cette possibilité.


## 3. Résultats de la campagne

10 cas prévus, 10 cas éxécutés :

- 6 OK
- 4 KO
- 1 NT


## 4. Réserves bloquantes

- ANO-005 : 
    - Cohérence indicateurs / routes get.
    - Modifier le code pour assurer cette cohérence.
    - Responsable : Thomas Lerond
    - échéance : 30/10/2026

## 5. Réserves non bloquantes

- ANO-001 : 
    - Journal d'audit.
    - Modifier le reporting de l'audit.
    - Responsable : Thomas Lerond
    - échéance : 30/10/2026

- ANO-002 : 
    - Chargement / Sauvegarde des datas csv.
    - Ecraser les datas après fiabilisation plutôt que de les sauvegarder sur un fichier à part.
    - Responsable : Thomas Lerond
    - échéance : 30/10/2026

- ANO-003 : 
    - Permission du jeton `Direction`.
    - Sécuriser la route `PUT /incidents/<id>/statut`, seul le jeton `exploitant` doit y avoir accès.
    - Responsable : Thomas Lerond
    - échéance : 30/10/2026

- ANO-004 : 
    - Pagination, réponses pages 0 et page 101 (i.d. en dehors de la dernière page affichable).
    - Le swagger doit fournir une réponse 422 pour les 2 commandes.
    - Responsable : Thomas Lerond
    - échéance : 30/10/2026

## 6. Décision
Recette PRONONCÉE AVEC RÉSERVES

La plupart des routes fonctionnent correctement, l'anomalie la plus grave est une erreur dans le calcul des indicateurs, à revopir en priorité. Les autres routes donnent lieu à des anomalies mineures.

## 7. Signatures
Pour le commanditaire — pour le développeur, le 15/10/2026.
```
Thomas Lerond
```
