# Projet VéloVille


## Bilan de la dernière fiabilisation (2026-10-13 13:47:46)

### 1. Synthèse par entité
| Entité | Lignes lues | Valides (Chargées) | Avertissements (Modifiées) | Rejets (Erreurs) |
| :--- | :---: | :---: | :---: | :---: |
| **Stations** | 120 | 120 | 0 | 0 |
| **Trajets** | 2030 | 2009 | 6 | 21 |
| **Incidents** | 180 | 177 | 177 | 3 |

### 2. Journal des rejets (Lignes exclues)

#### Trajets
- **Ligne 31** : Station d'arrivée inconnue ou invalide : 'S999'
- **Ligne 35** : Station d'arrivée inconnue ou invalide : 'S999'
- **Ligne 155** : Format d'horodatage invalide : '24/08/2026 11:01'
- **Ligne 238** : Station d'arrivée inconnue ou invalide : 'S999'
- **Ligne 384** : Format d'horodatage invalide : '25/08/2026 17:08'
- **Ligne 601** : duree_secondes doit être > 0 (valeur: -120)
- **Ligne 602** : duree_secondes doit être > 0 (valeur: -120)
- **Ligne 718** : duree_secondes doit être > 0 (valeur: -45)
- **Ligne 865** : Station d'arrivée inconnue ou invalide : 'S999'
- **Ligne 906** : duree_secondes doit être > 0 (valeur: -45)
- **Ligne 931** : duree_secondes doit être > 0 (valeur: -120)
- **Ligne 1075** : duree_secondes doit être > 0 (valeur: 0)
- **Ligne 1082** : duree_secondes doit être > 0 (valeur: 0)
- **Ligne 1282** : duree_secondes doit être > 0 (valeur: 0)
- **Ligne 1472** : Station d'arrivée inconnue ou invalide : 'S999'
- **Ligne 1600** : Format d'horodatage invalide : '29/08/2026 12:59'
- **Ligne 1698** : duree_secondes doit être > 0 (valeur: -120)
- **Ligne 1727** : Station d'arrivée inconnue ou invalide : 'S999'
- **Ligne 1858** : duree_secondes doit être > 0 (valeur: -45)
- **Ligne 1897** : Format d'horodatage invalide : '30/08/2026 07:22'
- **Ligne 1971** : Format d'horodatage invalide : '30/08/2026 15:22'

#### Incidents
- **Ligne 29** : date_resolution ne peut pas être antérieure à date_signalement.
- **Ligne 125** : date_resolution ne peut pas être antérieure à date_signalement.
- **Ligne 179** : date_resolution ne peut pas être antérieure à date_signalement.

### 3. Journal des avertissements (Lignes conservées mais modifiées)

#### Trajets
- **Ligne 89** : Identifiant 'velo_id' passé en majuscules ('v1281' -> 'V1281')
- **Ligne 611** : Identifiant 'velo_id' passé en majuscules ('v0685' -> 'V0685')
- **Ligne 936** : Identifiant 'velo_id' passé en majuscules ('v0800' -> 'V0800')
- **Ligne 1367** : Identifiant 'velo_id' passé en majuscules ('v0959' -> 'V0959')
- **Ligne 1695** : Identifiant 'velo_id' passé en majuscules ('v1788' -> 'V1788')
- **Ligne 1919** : Identifiant 'velo_id' passé en majuscules ('v0936' -> 'V0936')

#### Incidents
- **Ligne 2** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 3** : Date reformatée au standard valide ('2026-08-26 20:00' -> '2026-08-26 20:00:00')
- **Ligne 4** : Date reformatée au standard valide ('2026-07-04 13:00' -> '2026-07-04 13:00:00')
- **Ligne 5** : Date reformatée au standard valide ('2026-07-08 10:00' -> '2026-07-08 10:00:00')
- **Ligne 6** : Date reformatée au standard valide ('2026-08-09 09:00' -> '2026-08-09 09:00:00')
- **Ligne 7** : Date reformatée au standard valide ('2026-07-15 11:00' -> '2026-07-15 11:00:00')
- **Ligne 8** : Date reformatée au standard valide ('2026-08-05 18:00' -> '2026-08-05 18:00:00')
- **Ligne 9** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 10** : Date reformatée au standard valide ('2026-08-25 14:00' -> '2026-08-25 14:00:00')
- **Ligne 11** : Date reformatée au standard valide ('2026-07-13 09:00' -> '2026-07-13 09:00:00')
- **Ligne 12** : Date reformatée au standard valide ('2026-07-15 13:00' -> '2026-07-15 13:00:00')
- **Ligne 13** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 14** : Date reformatée au standard valide ('2026-07-24 20:00' -> '2026-07-24 20:00:00')
- **Ligne 15** : Date reformatée au standard valide ('2026-08-17 19:00' -> '2026-08-17 19:00:00')
- **Ligne 16** : Date reformatée au standard valide ('2026-07-14 16:00' -> '2026-07-14 16:00:00')
- **Ligne 17** : Date reformatée au standard valide ('2026-08-11 17:00' -> '2026-08-11 17:00:00')
- **Ligne 18** : Date reformatée au standard valide ('2026-07-22 11:00' -> '2026-07-22 11:00:00')
- **Ligne 19** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 20** : Date reformatée au standard valide ('2026-07-22 10:00' -> '2026-07-22 10:00:00')
- **Ligne 21** : Date reformatée au standard valide ('2026-08-19 16:00' -> '2026-08-19 16:00:00')
- **Ligne 22** : Date reformatée au standard valide ('2026-08-16 18:00' -> '2026-08-16 18:00:00')
- **Ligne 23** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 24** : Date reformatée au standard valide ('2026-08-07 19:00' -> '2026-08-07 19:00:00')
- **Ligne 25** : Date reformatée au standard valide ('2026-07-14 11:00' -> '2026-07-14 11:00:00')
- **Ligne 26** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 27** : Date reformatée au standard valide ('2026-07-10 16:00' -> '2026-07-10 16:00:00')
- **Ligne 28** : Date reformatée au standard valide ('2026-08-11 13:00' -> '2026-08-11 13:00:00')
- **Ligne 30** : Date reformatée au standard valide ('2026-07-06 15:00' -> '2026-07-06 15:00:00')
- **Ligne 31** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 32** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 33** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 34** : Date reformatée au standard valide ('2026-07-29 13:00' -> '2026-07-29 13:00:00')
- **Ligne 35** : Date reformatée au standard valide ('2026-08-26 09:00' -> '2026-08-26 09:00:00')
- **Ligne 36** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 37** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 38** : Date reformatée au standard valide ('2026-08-28 13:00' -> '2026-08-28 13:00:00')
- **Ligne 39** : Date reformatée au standard valide ('2026-07-13 19:00' -> '2026-07-13 19:00:00')
- **Ligne 40** : Date reformatée au standard valide ('2026-08-30 15:00' -> '2026-08-30 15:00:00')
- **Ligne 41** : Date reformatée au standard valide ('2026-07-08 12:00' -> '2026-07-08 12:00:00')
- **Ligne 42** : Date reformatée au standard valide ('2026-07-18 12:00' -> '2026-07-18 12:00:00')
- **Ligne 43** : Date reformatée au standard valide ('2026-08-11 13:00' -> '2026-08-11 13:00:00')
- **Ligne 44** : Date reformatée au standard valide ('2026-07-31 10:00' -> '2026-07-31 10:00:00')
- **Ligne 45** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 46** : Date reformatée au standard valide ('2026-07-10 15:00' -> '2026-07-10 15:00:00')
- **Ligne 47** : Date reformatée au standard valide ('2026-07-18 15:00' -> '2026-07-18 15:00:00')
- **Ligne 48** : Date reformatée au standard valide ('2026-08-20 18:00' -> '2026-08-20 18:00:00')
- **Ligne 49** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 50** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 51** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 52** : Date reformatée au standard valide ('2026-07-17 07:00' -> '2026-07-17 07:00:00')
- **Ligne 53** : Date reformatée au standard valide ('2026-07-17 07:00' -> '2026-07-17 07:00:00')
- **Ligne 54** : Date reformatée au standard valide ('2026-07-04 14:00' -> '2026-07-04 14:00:00')
- **Ligne 55** : Date reformatée au standard valide ('2026-08-11 08:00' -> '2026-08-11 08:00:00')
- **Ligne 56** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 57** : Date reformatée au standard valide ('2026-07-18 15:00' -> '2026-07-18 15:00:00')
- **Ligne 58** : Date reformatée au standard valide ('2026-08-19 15:00' -> '2026-08-19 15:00:00')
- **Ligne 59** : Date reformatée au standard valide ('2026-08-28 18:00' -> '2026-08-28 18:00:00')
- **Ligne 60** : Date reformatée au standard valide ('2026-08-08 15:00' -> '2026-08-08 15:00:00')
- **Ligne 61** : Date reformatée au standard valide ('2026-08-20 16:00' -> '2026-08-20 16:00:00')
- **Ligne 62** : Date reformatée au standard valide ('2026-08-12 16:00' -> '2026-08-12 16:00:00')
- **Ligne 63** : Date reformatée au standard valide ('2026-07-03 10:00' -> '2026-07-03 10:00:00')
- **Ligne 64** : Date reformatée au standard valide ('2026-07-28 19:00' -> '2026-07-28 19:00:00')
- **Ligne 65** : Date reformatée au standard valide ('2026-08-28 14:00' -> '2026-08-28 14:00:00')
- **Ligne 66** : Date reformatée au standard valide ('2026-08-29 13:00' -> '2026-08-29 13:00:00')
- **Ligne 67** : Date reformatée au standard valide ('2026-07-08 09:00' -> '2026-07-08 09:00:00')
- **Ligne 68** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 69** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 70** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 71** : Date reformatée au standard valide ('2026-07-01 18:00' -> '2026-07-01 18:00:00')
- **Ligne 72** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 73** : Date reformatée au standard valide ('2026-07-09 16:00' -> '2026-07-09 16:00:00')
- **Ligne 74** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 75** : Date reformatée au standard valide ('2026-07-29 18:00' -> '2026-07-29 18:00:00')
- **Ligne 76** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 77** : Date reformatée au standard valide ('2026-07-04 10:00' -> '2026-07-04 10:00:00')
- **Ligne 78** : Date reformatée au standard valide ('2026-07-30 08:00' -> '2026-07-30 08:00:00')
- **Ligne 79** : Date reformatée au standard valide ('2026-08-20 07:00' -> '2026-08-20 07:00:00')
- **Ligne 80** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 81** : Date reformatée au standard valide ('2026-07-25 11:00' -> '2026-07-25 11:00:00')
- **Ligne 82** : Date reformatée au standard valide ('2026-07-17 12:00' -> '2026-07-17 12:00:00')
- **Ligne 83** : Date reformatée au standard valide ('2026-07-03 13:00' -> '2026-07-03 13:00:00')
- **Ligne 84** : Date reformatée au standard valide ('2026-08-17 18:00' -> '2026-08-17 18:00:00')
- **Ligne 85** : Date reformatée au standard valide ('2026-07-29 15:00' -> '2026-07-29 15:00:00')
- **Ligne 86** : Date reformatée au standard valide ('2026-07-17 16:00' -> '2026-07-17 16:00:00')
- **Ligne 87** : Date reformatée au standard valide ('2026-07-31 07:00' -> '2026-07-31 07:00:00')
- **Ligne 88** : Date reformatée au standard valide ('2026-07-31 18:00' -> '2026-07-31 18:00:00')
- **Ligne 89** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 90** : Date reformatée au standard valide ('2026-07-17 13:00' -> '2026-07-17 13:00:00')
- **Ligne 91** : Date reformatée au standard valide ('2026-08-01 09:00' -> '2026-08-01 09:00:00')
- **Ligne 92** : Date reformatée au standard valide ('2026-07-28 20:00' -> '2026-07-28 20:00:00')
- **Ligne 93** : Date reformatée au standard valide ('2026-07-27 11:00' -> '2026-07-27 11:00:00')
- **Ligne 94** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 95** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 96** : Date reformatée au standard valide ('2026-07-10 07:00' -> '2026-07-10 07:00:00')
- **Ligne 97** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 98** : Date reformatée au standard valide ('2026-07-15 09:00' -> '2026-07-15 09:00:00')
- **Ligne 99** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 100** : Date reformatée au standard valide ('2026-08-13 09:00' -> '2026-08-13 09:00:00')
- **Ligne 101** : Date reformatée au standard valide ('2026-07-05 17:00' -> '2026-07-05 17:00:00')
- **Ligne 102** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 103** : Date reformatée au standard valide ('2026-07-17 18:00' -> '2026-07-17 18:00:00')
- **Ligne 104** : Date reformatée au standard valide ('2026-08-29 12:00' -> '2026-08-29 12:00:00')
- **Ligne 105** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 106** : Date reformatée au standard valide ('2026-08-01 07:00' -> '2026-08-01 07:00:00')
- **Ligne 107** : Date reformatée au standard valide ('2026-07-20 13:00' -> '2026-07-20 13:00:00')
- **Ligne 108** : Date reformatée au standard valide ('2026-07-10 10:00' -> '2026-07-10 10:00:00')
- **Ligne 109** : Date reformatée au standard valide ('2026-07-10 08:00' -> '2026-07-10 08:00:00')
- **Ligne 110** : Date reformatée au standard valide ('2026-08-23 18:00' -> '2026-08-23 18:00:00')
- **Ligne 111** : Date reformatée au standard valide ('2026-08-08 17:00' -> '2026-08-08 17:00:00')
- **Ligne 112** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 113** : Date reformatée au standard valide ('2026-08-03 14:00' -> '2026-08-03 14:00:00')
- **Ligne 114** : Date reformatée au standard valide ('2026-07-13 08:00' -> '2026-07-13 08:00:00')
- **Ligne 115** : Date reformatée au standard valide ('2026-08-03 14:00' -> '2026-08-03 14:00:00')
- **Ligne 116** : Date reformatée au standard valide ('2026-08-06 20:00' -> '2026-08-06 20:00:00')
- **Ligne 117** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 118** : Date reformatée au standard valide ('2026-08-16 17:00' -> '2026-08-16 17:00:00')
- **Ligne 119** : Date reformatée au standard valide ('2026-08-17 18:00' -> '2026-08-17 18:00:00')
- **Ligne 120** : Date reformatée au standard valide ('2026-07-31 12:00' -> '2026-07-31 12:00:00')
- **Ligne 121** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 122** : Date reformatée au standard valide ('2026-07-31 13:00' -> '2026-07-31 13:00:00')
- **Ligne 123** : Date reformatée au standard valide ('2026-07-22 18:00' -> '2026-07-22 18:00:00')
- **Ligne 124** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 126** : Date reformatée au standard valide ('2026-08-27 10:00' -> '2026-08-27 10:00:00')
- **Ligne 127** : Date reformatée au standard valide ('2026-08-12 16:00' -> '2026-08-12 16:00:00')
- **Ligne 128** : Date reformatée au standard valide ('2026-08-29 16:00' -> '2026-08-29 16:00:00')
- **Ligne 129** : Date reformatée au standard valide ('2026-07-19 07:00' -> '2026-07-19 07:00:00')
- **Ligne 130** : Date reformatée au standard valide ('2026-08-22 10:00' -> '2026-08-22 10:00:00')
- **Ligne 131** : Date reformatée au standard valide ('2026-07-08 08:00' -> '2026-07-08 08:00:00')
- **Ligne 132** : Date reformatée au standard valide ('2026-07-14 15:00' -> '2026-07-14 15:00:00')
- **Ligne 133** : Date reformatée au standard valide ('2026-08-05 11:00' -> '2026-08-05 11:00:00')
- **Ligne 134** : Date reformatée au standard valide ('2026-07-22 15:00' -> '2026-07-22 15:00:00')
- **Ligne 135** : Date reformatée au standard valide ('2026-07-01 14:00' -> '2026-07-01 14:00:00')
- **Ligne 136** : Date reformatée au standard valide ('2026-08-23 10:00' -> '2026-08-23 10:00:00')
- **Ligne 137** : Date reformatée au standard valide ('2026-07-18 09:00' -> '2026-07-18 09:00:00')
- **Ligne 138** : Date reformatée au standard valide ('2026-07-02 11:00' -> '2026-07-02 11:00:00')
- **Ligne 139** : Date reformatée au standard valide ('2026-07-19 18:00' -> '2026-07-19 18:00:00')
- **Ligne 140** : Date reformatée au standard valide ('2026-08-20 07:00' -> '2026-08-20 07:00:00')
- **Ligne 141** : Date reformatée au standard valide ('2026-08-22 15:00' -> '2026-08-22 15:00:00')
- **Ligne 142** : Date reformatée au standard valide ('2026-08-12 07:00' -> '2026-08-12 07:00:00')
- **Ligne 143** : Date reformatée au standard valide ('2026-08-18 11:00' -> '2026-08-18 11:00:00')
- **Ligne 144** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 145** : Date reformatée au standard valide ('2026-08-16 19:00' -> '2026-08-16 19:00:00')
- **Ligne 146** : Date reformatée au standard valide ('2026-08-08 14:00' -> '2026-08-08 14:00:00')
- **Ligne 147** : Date reformatée au standard valide ('2026-08-11 13:00' -> '2026-08-11 13:00:00')
- **Ligne 148** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 149** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 150** : Date reformatée au standard valide ('2026-07-21 12:00' -> '2026-07-21 12:00:00')
- **Ligne 151** : Date reformatée au standard valide ('2026-07-20 17:00' -> '2026-07-20 17:00:00')
- **Ligne 152** : Date reformatée au standard valide ('2026-08-24 17:00' -> '2026-08-24 17:00:00')
- **Ligne 153** : Date reformatée au standard valide ('2026-08-27 09:00' -> '2026-08-27 09:00:00')
- **Ligne 154** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 155** : Date reformatée au standard valide ('2026-08-03 16:00' -> '2026-08-03 16:00:00')
- **Ligne 156** : Date reformatée au standard valide ('2026-08-13 09:00' -> '2026-08-13 09:00:00')
- **Ligne 157** : Date reformatée au standard valide ('2026-08-26 17:00' -> '2026-08-26 17:00:00')
- **Ligne 158** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 159** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 160** : Date reformatée au standard valide ('2026-07-23 08:00' -> '2026-07-23 08:00:00')
- **Ligne 161** : Date reformatée au standard valide ('2026-08-24 07:00' -> '2026-08-24 07:00:00')
- **Ligne 162** : Date reformatée au standard valide ('2026-08-15 09:00' -> '2026-08-15 09:00:00')
- **Ligne 163** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 164** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 165** : Date reformatée au standard valide ('2026-08-25 18:00' -> '2026-08-25 18:00:00')
- **Ligne 166** : Date reformatée au standard valide ('2026-07-03 16:00' -> '2026-07-03 16:00:00')
- **Ligne 167** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 168** : Date reformatée au standard valide ('2026-08-10 09:00' -> '2026-08-10 09:00:00')
- **Ligne 169** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 170** : Date reformatée au standard valide ('2026-07-08 09:00' -> '2026-07-08 09:00:00')
- **Ligne 171** : Date reformatée au standard valide ('2026-08-10 16:00' -> '2026-08-10 16:00:00')
- **Ligne 172** : Date reformatée au standard valide ('2026-08-10 20:00' -> '2026-08-10 20:00:00')
- **Ligne 173** : Date reformatée au standard valide ('2026-08-13 16:00' -> '2026-08-13 16:00:00')
- **Ligne 174** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 175** : Statut corrigé de 'en cours' vers 'en_cours'
- **Ligne 176** : Date reformatée au standard valide ('2026-07-28 20:00' -> '2026-07-28 20:00:00')
- **Ligne 177** : Date reformatée au standard valide ('2026-07-19 20:00' -> '2026-07-19 20:00:00')
- **Ligne 178** : Date reformatée au standard valide ('2026-08-26 08:00' -> '2026-08-26 08:00:00')
- **Ligne 180** : Date reformatée au standard valide ('2026-08-01 15:00' -> '2026-08-01 15:00:00')
- **Ligne 181** : Date reformatée au standard valide ('2026-08-23 14:00' -> '2026-08-23 14:00:00')
