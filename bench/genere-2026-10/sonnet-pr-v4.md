## Refactorisation du module d'envoi d'emails

### Contexte

La logique d'envoi d'emails était dispersée entre plusieurs mailers, des callbacks de modèles et des appels directs à `deliver_now` dans les contrôleurs. Cela rendait le code difficile à tester, à faire évoluer et à surveiller.

### Changements

- **Mailers** : création d'un `ApplicationMailer` enrichi (expéditeur par défaut, layout commun, helpers partagés). Les mailers existants en héritent et ne contiennent plus de logique métier.
- **Service d'envoi** : ajout de `EmailDispatcher`, point d'entrée unique pour l'envoi. Il centralise la gestion des erreurs, les logs et les tentatives de renvoi.
- **Envoi asynchrone** : tous les envois passent désormais par `deliver_later` via Active Job (queue `mailers`). Suppression des `deliver_now` dans les contrôleurs.
- **Callbacks** : retrait des envois d'emails depuis les callbacks `after_create` / `after_save` des modèles, remplacés par des appels explicites dans les services.
- **Templates** : factorisation des vues en partials (en-tête, pied de page, boutons) et passage des textes en I18n (`fr` et `en`).
- **Configuration** : paramètres SMTP et URL par défaut regroupés par environnement. Ajout de `letter_opener` en développement.
- **Prévisualisations** : ajout de `ActionMailer::Preview` pour chaque email.

### Impact

- Aucun changement visible pour les utilisateurs : le contenu et les destinataires des emails restent identiques.
- Les emails ne bloquent plus le cycle requête/réponse.
- Nécessite un worker Active Job actif sur la queue `mailers` en production.

### Tests

- Mise à jour des specs de mailers (RSpec) et ajout de specs pour `EmailDispatcher`.
- Ajout de tests d'intégration vérifiant la mise en file des jobs.
- Suite complète passante en local et en CI.

### Points d'attention pour la relecture

- Vérifier que la queue `mailers` est bien consommée dans l'environnement cible avant le déploiement.
- Vérifier qu'aucun envoi n'est dupliqué suite au retrait des callbacks.

### Checklist

- [x] Tests ajoutés / mis à jour
- [x] Rubocop sans erreur
- [x] Pas de migration
- [ ] Vérification de la configuration des workers en staging
