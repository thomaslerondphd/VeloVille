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
- Le journal ne donne pas les infrmations sous la forme attendue
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

### Statut
