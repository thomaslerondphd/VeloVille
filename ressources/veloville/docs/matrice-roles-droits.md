# Matrice rôles x droits

À compléter : une ligne par route, une colonne par rôle (anonyme, exploitant,
direction), code HTTP attendu en cas de refus.

---
| Route | anonyme | exploitant | direction |
| --- | --- | --- | --- |
| /sante	GET | Autorisé | Autorisé | Autorisé |
| /auth/login	POST | Autorisé	| Autorisé	| Autorisé |	
| /stations	GET	| Refusé	| Autorisé	| Autorisé |
| /stations/{station_id}	GET	| Refusé	| Autorisé	| Autorisé |
| /trajets	GET	| Refusé	| Autorisé	| Autorisé	|
| /incidents	GET	| Refusé	| Autorisé	| Autorisé	|
| /incidents/{incident_id}/statut	PUT	| Refusé	| Autorisé	| Refusé |
| /indicateurs/activite-par-jour	GET	| Refusé	| Autorisé	| Autorisé	|
| /indicateurs/stations-actives	GET	| Refusé	| Autorisé	| Autorisé	|
| /indicateurs/incidents-par-statut	GET	| Refusé	| Autorisé	| Autorisé	|