# Dictionnaire des données — exports VéloVille

Trois fichiers CSV sont fournis dans `donnees/` (et recopiés dans `data/`
du squelette). Séparateur : virgule ; encodage : UTF-8 ; première ligne :
en-têtes ; valeurs absentes : champ vide.

**Avertissement.** Ces fichiers sont des exports bruts du système de
billettique de VéloVille. Ils n'ont fait l'objet d'aucune fiabilisation :
formats, casse, cohérence entre colonnes et entre fichiers ne sont pas
garantis. Les formats et valeurs indiqués ci-dessous sont les formats
**attendus** par le cahier des charges, pas une description de ce que
contiennent effectivement les fichiers. L'audit et la fiabilisation font
partie du travail demandé.

## stations.csv — référentiel des stations

120 lignes. Une ligne par station en service.

| Colonne | Type attendu | Description |
|---|---|---|
| station_id | texte, `S` + 3 chiffres (ex. `S001`) | Identifiant unique de la station |
| nom | texte | Nom d'usage : commune et lieu (ex. `Lille - Gare`) |
| commune | texte | Commune d'implantation (9 communes de la métropole) |
| capacite | entier > 0 | Nombre de points d'attache |
| latitude | décimal, 5 décimales | Coordonnée WGS84 |
| longitude | décimal, 5 décimales | Coordonnée WGS84 |
| date_mise_en_service | date `AAAA-MM-JJ` | Date d'ouverture de la station |

## trajets.csv — trajets de la semaine du 24 au 30 août 2026

2 030 lignes. Une ligne par location de vélo. Extrait d'une semaine.

| Colonne | Type attendu | Description |
|---|---|---|
| trajet_id | texte, `T` + 6 chiffres (ex. `T480001`) | Identifiant unique du trajet |
| velo_id | texte, `V` + 4 chiffres (ex. `V1167`) | Identifiant du vélo emprunté |
| depart_horodatage | horodatage `AAAA-MM-JJ HH:MM:SS` | Date et heure de retrait du vélo |
| station_depart | référence `station_id` | Station de retrait (obligatoire) |
| station_arrivee | référence `station_id`, ou vide | Station de restitution ; vide si le vélo n'était pas restitué au moment de l'export |
| duree_secondes | entier > 0 | Durée de la location en secondes |
| type_usager | `abonne` ou `occasionnel` | Type d'usager |
| usager_ref | texte, `U` + 8 caractères hexadécimaux, ou vide | Pseudonyme de l'abonné (hachage tronqué du numéro d'abonné) ; toujours vide pour un usager occasionnel |

## incidents.csv — incidents de maintenance du 1er juillet au 30 août 2026

180 lignes. Une ligne par incident signalé.

| Colonne | Type attendu | Description |
|---|---|---|
| incident_id | texte, `I2026-` + 4 chiffres (ex. `I2026-0001`) | Identifiant unique de l'incident |
| date_signalement | horodatage `AAAA-MM-JJ HH:MM` | Date et heure du signalement |
| cible | `velo` ou `station` | Nature de l'équipement concerné |
| velo_id | référence vélo, ou vide | Renseigné si et seulement si `cible` = `velo` |
| station_id | référence `station_id`, ou vide | Renseigné si et seulement si `cible` = `station` |
| type_incident | texte | Catégorie : `vandalisme`, `selle abimee`, `eclairage HS`, `chaine deraillee`, `ecran borne illisible`, `pneu creve`, `frein defectueux`, `borne hors service` |
| statut | `ouvert`, `en_cours` ou `resolu` | État de traitement |
| date_resolution | horodatage `AAAA-MM-JJ HH:MM`, ou vide | Renseignée si et seulement si le statut est `resolu` ; postérieure ou égale au signalement |
| technicien | texte, ou vide | Technicien en charge ; renseigné en principe dès la prise en charge |

## Liens entre les fichiers

- `trajets.station_depart` et `trajets.station_arrivee` référencent
  `stations.station_id`.
- `incidents.station_id` référence `stations.station_id`.
- Les vélos n'ont pas de fichier de référence : `velo_id` est une simple
  chaîne, dont le format attendu est `V` suivi de quatre chiffres.

## Remarques utiles pour l'audit

- Comparez les valeurs distinctes de chaque colonne à son domaine attendu
  (`sort | uniq -c`, `value_counts()`).
- Vérifiez l'unicité des identifiants et l'absence de lignes dupliquées.
- Vérifiez les références croisées entre fichiers.
- Vérifiez la cohérence des dates entre colonnes d'un même fichier.
- Consignez chaque défaut trouvé avec le nombre de lignes concernées et le
  traitement retenu : c'est cette trace qui est attendue dans votre dossier.
