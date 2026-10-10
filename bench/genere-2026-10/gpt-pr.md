## Résumé

Cette pull request ajoute un cache Redis devant l’API de recherche Django afin de réduire les temps de réponse et la charge sur la base de données.

## Modifications

- Mise en cache des résultats selon les paramètres de recherche.
- Configuration d’une durée de vie pour éviter les données obsolètes.
- Contournement automatique du cache en cas d’indisponibilité de Redis.
- Invalidation du cache lors des mises à jour susceptibles d’affecter les résultats.
- Ajout de tests couvrant les succès, les expirations et les erreurs Redis.

## Impact

Les recherches répétées sont désormais servies depuis Redis, sans modification du contrat de l’API. Le premier appel reste inchangé, tandis que les appels suivants bénéficient d’une latence réduite.

## Configuration

Redis doit être accessible via la variable d’environnement `REDIS_URL`.