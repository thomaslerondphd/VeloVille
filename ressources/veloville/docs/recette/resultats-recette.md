# Résultats de recette

## REC-01 — Import idempotent
1. 2. Première éxécution :
-> Stations importées : 120 / 120 
-> Trajets importés : 2009 / 2030
-> Incidents importés : 177 / 180

3. 4. Seconde éxécution : 
-> Stations importées : 120 / 120
-> Trajets importés : 2009 / 2030
-> Incidents importés : 177 / 180

### Résultat attendu
- Les deux exécutions se terminent sans erreur
- les trois comptages sont identiques entre les étapes 2 et 4 
- `count(*) FROM station` vaut 120.

### Résultat obtenu

extrait de rapport du rapport de fiabilisation :
![alt text](image-1.png)


- Les deux exécutions se terminent sans erreur **OK**
- les trois comptages sont identiques entre les étapes 2 et 4 **OK**
- `count(*) FROM station` vaut 120 **OK**

### Statut
OK

## REC-02 — Rejets journalisés et cohérence des volumes

### Résultat attendu

Pour chaque fichier : importées + rejetées + doublons écartés = lignes du CSV. Chaque ligne du journal porte les six informations. La requête de l'étape 4 renvoie 0.

### Résultat obtenu

![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)

### Statut
KO :
- Le journal ne donne pas les informations sous la forme attendue
- Relancer le fichier `importer.py` relance tout le processus depuis les données brutes et ne reprend pas les données nettoyées ; l'étape 4 donne donc le même résultat que l'étape 2

## REC-03 — Connexion acceptée

### Résultat obtenu

![alt text](image-5.png)
![alt text](image-6.png)

![alt text](image-7.png)
![alt text](image-8.png)

### Statut

OK

## REC-04 — Connexion refusée

### Résultat obtenu
![alt text](image-9.png)
![alt text](image-10.png)

### Statut

OK

## REC-05 — Route protégée sans jeton

### Résultat obtenu
![alt text](image-11.png)
![alt text](image-12.png)
 
### Statut

OK

## REC-06 — Rôle direction refusé sur la modification d'un incident

### Résultat obtenu
![alt text](image-13.png)
- le jeton direction permet la modification de statut d'un incident.
![alt text](image-14.png)
- Refaire la même demande une seconde fois donne une réponse 422

### Statut

KO

## REC-07 — Pagination

### Résultat obtenu

1. ![alt text](image-15.png)
2. ![alt text](image-16.png)
3. ![alt text](image-17.png)
4. ![alt text](image-18.png)
le swagger donne la page 0 comme incorrecte
5. ![alt text](image-19.png)
le swagger affiche une réponse 200 avec liste vide

### Statut

KO

## REC-08 — Station introuvable

### Résultat obtenu

1. ![alt text](image-21.png)
2. ![alt text](image-22.png)

### Statut

OK

## REC-09 — Cohérence de l'indicateur « activité par jour » avec la base

### Résultat obtenu

1. ![alt text](image-23.png)
2. ![alt text](image-24.png)
3. lignes exactement les mêmes
4. `GET /trajets?date_debut=2026-08-24&date_fin=2026-08-30` `total : 1998`
```
Somme des indicateurs récupérés : 
S = 329 + 310 + 306 + 300 + 315 + 218 + 220
S = 2028
```
![alt text](image-25.png)

### Statut

KO

## REC-10 — Front : état vide et état d'erreur

### Résultat obtenu

1. ![alt text](image-26.png) NT : Le frontend ne prévoit pas de filtrer par le statut de l'incident
2. 3. ![alt text](image-27.png)
4. ![alt text](image-28.png)
5. ![alt text](image-29.png)

### Statut

OK