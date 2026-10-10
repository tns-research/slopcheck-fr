## Ajout d'un cache Redis devant l'API de recherche

### Contexte

L'endpoint `/api/search/` interroge directement la base de données à chaque appel. Aux heures de pointe, les mêmes requêtes reviennent très souvent : le temps de réponse se dégrade et la charge sur PostgreSQL augmente sans raison.

### Changements

- Ajout de Redis comme backend de cache Django (`django-redis`), configuré via la variable d'environnement `REDIS_URL`.
- Mise en cache des résultats de recherche dans `SearchView` :
  - la clé est construite à partir des paramètres normalisés de la requête (terme, filtres, tri, pagination), puis hachée ;
  - la durée de vie est configurable avec `SEARCH_CACHE_TTL` (300 secondes par défaut).
- Invalidation : un signal `post_save` / `post_delete` sur les modèles indexés incrémente un numéro de version inclus dans les clés. Les anciennes entrées ne sont donc plus jamais lues et expirent d'elles-mêmes.
- Repli en cas de panne : si Redis est indisponible, la vue interroge directement la base et journalise un avertissement, sans renvoyer d'erreur au client.
- Ajout d'un en-tête `X-Cache: HIT|MISS` pour faciliter le débogage.
- Ajout du service `redis` dans `docker-compose.yml` pour le développement local.

### Tests

- Tests unitaires sur la génération des clés : deux requêtes équivalentes dont les paramètres sont dans un ordre différent produisent la même clé.
- Tests d'intégration : le premier appel donne un MISS et le second un HIT, et toute modification d'un objet indexé invalide le cache.
- Test du repli : on simule une `ConnectionError` Redis et la réponse reste correcte.
- Mesure locale avec `locust` (100 utilisateurs, requêtes répétées) : latence p95 passée d'environ 420 ms à environ 35 ms en HIT.

### Déploiement

1. Provisionner une instance Redis et renseigner `REDIS_URL` dans les variables d'environnement.
2. Optionnel : ajuster `SEARCH_CACHE_TTL`.
3. Aucune migration de base de données n'est nécessaire.

### Points d'attention

- Les résultats peuvent rester obsolètes au plus pendant le TTL si une donnée change sans passer par l'ORM (import SQL brut, par exemple). Dans ce cas, lancer `python manage.py clear_search_cache`.
- Les recherches d'utilisateurs authentifiés dont les résultats dépendent des permissions ne sont pas mises en cache dans cette PR.
