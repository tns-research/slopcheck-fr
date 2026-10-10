## Ajout d'un cache Redis devant l'API de recherche

### Contexte

L'endpoint `/api/search/` est l'un des plus sollicités de l'application. Chaque requête déclenche des requêtes SQL coûteuses (filtres, tri, pagination), alors que de nombreuses recherches sont identiques d'un appel à l'autre. Cette PR met les résultats en cache dans Redis pour réduire la charge sur la base et la latence.

### Changements

- Ajout de `django-redis` comme backend de cache (`CACHES` dans les settings, configuré via la variable d'environnement `REDIS_URL`).
- Nouveau module `search/cache.py` :
  - construction de la clé de cache à partir des paramètres normalisés de la requête (requête texte, filtres, tri, page), triés et hachés pour éviter les doublons ;
  - helpers `get_cached_results` et `set_cached_results`.
- `SearchView` consulte le cache avant d'interroger la base et stocke le résultat en cas de miss.
- TTL par défaut de 5 minutes, configurable via `SEARCH_CACHE_TTL`.
- Invalidation : les signaux `post_save` et `post_delete` des modèles indexés incrémentent un numéro de version inclus dans la clé, ce qui invalide d'un coup tous les résultats concernés.
- Ajout d'un en-tête de réponse `X-Cache: HIT|MISS` pour faciliter le débogage et le suivi.
- Dégradation gracieuse : si Redis est indisponible, l'erreur est loggée et la requête est servie directement depuis la base, sans erreur côté client.

### Choix de conception

- Un numéro de version plutôt qu'une suppression de clés par motif : évite les `SCAN`/`KEYS` coûteux sur Redis.
- Les résultats dépendant de l'utilisateur (permissions, favoris) ne sont pas mis en cache pour éviter toute fuite de données entre comptes. La clé inclut l'identifiant de périmètre d'accès, et les requêtes authentifiées avec résultats personnalisés contournent le cache.

### Comment tester

1. Lancer Redis en local : `docker run -p 6379:6379 redis:7`.
2. Définir `REDIS_URL=redis://localhost:6379/0`.
3. Appeler deux fois `/api/search/?q=test` : le premier appel renvoie `X-Cache: MISS`, le second `X-Cache: HIT`.
4. Modifier un objet indexé puis rappeler l'endpoint : retour à `MISS`.
5. Arrêter Redis : l'API continue de répondre normalement.
6. Lancer les tests : `pytest search/tests/test_cache.py`.

### Points d'attention

- Redis devient une dépendance d'infrastructure optionnelle mais recommandée en production (à provisionner avant le déploiement).
- Prévoir un suivi du taux de hit après la mise en production pour ajuster le TTL.

### Checklist

- [x] Tests unitaires et d'intégration ajoutés
- [x] Documentation mise à jour (`README`, variables d'environnement)
- [x] Comportement vérifié avec Redis indisponible

🤖 Generated with [Claude Code](https://claude.com/claude-code)
