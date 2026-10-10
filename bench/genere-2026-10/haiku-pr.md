Ajoute un cache Redis devant l'API de recherche, avec invalidation à l'écriture et TTL configurable.

## Contexte
L'API de recherche interroge la base à chaque requête, ce qui pèse sur PostgreSQL quand les mêmes requêtes reviennent souvent. Cette PR ajoute un cache Redis devant l'endpoint de recherche pour réduire la charge et la latence.

## Changements
- Ajout d'un backend de cache Redis (client configuré via `settings`, variable `REDIS_URL`).
- Mise en cache des réponses de l'endpoint de recherche, avec une clé dérivée des paramètres normalisés (requête, filtres, pagination, tri).
- TTL configurable (`SEARCH_CACHE_TTL`, 300 s par défaut).
- Invalidation lors de la création, modification ou suppression d'un objet indexable (signaux Django `post_save` / `post_delete`), par versionnement de l'espace de clés pour éviter les `KEYS`/`SCAN` coûteux.
- Un flag `SEARCH_CACHE_ENABLED` permet de désactiver le cache sans redéploiement de code.

## Points d'attention
- Un résultat peut rester jusqu'à `SEARCH_CACHE_TTL` secondes obsolète si une écriture passe hors ORM (requête SQL brute, bulk update, migration).
- Si Redis est indisponible, la recherche retombe sur la base et un avertissement est journalisé ; aucune erreur n'est remontée à l'utilisateur.
- Les réponses mises en cache ne contiennent aucune donnée spécifique à l'utilisateur. Si des permissions par utilisateur sont ajoutées plus tard, la clé devra inclure l'identifiant utilisateur.

## Tests
- Tests unitaires du calcul de clé de cache et de la normalisation des paramètres.
- Tests d'intégration : cache hit / miss, invalidation après écriture, comportement lorsque Redis est indisponible.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
