## Refactorisation du module d'envoi d'emails

### Contexte

La logique d'envoi d'emails était dispersée entre les contrôleurs, les modèles (callbacks `after_create`) et plusieurs mailers qui dupliquaient la même configuration. Il était donc difficile de tester les envois, de savoir quel email partait à quel moment et d'ajouter un nouveau type de notification sans risque de régression.

### Changements

- **Mailers** : création d'un `ApplicationMailer` commun pour l'expéditeur par défaut, le layout, les en-têtes et le `reply_to`. Les mailers existants (`UserMailer`, `OrderMailer`, `InvoiceMailer`) en héritent et ne contiennent plus de configuration dupliquée.
- **Service objects** : les déclenchements d'emails passent par des services dédiés dans `app/services/notifications/` (par exemple `Notifications::OrderConfirmation`). Ces services remplacent les callbacks de modèles et les appels directs dans les contrôleurs.
- **Envoi asynchrone** : tous les emails sont envoyés avec `deliver_later`, via la queue `mailers` d'Active Job. Les erreurs SMTP temporaires sont rejouées avec `retry_on`, avec un backoff exponentiel.
- **Templates** : les partials communs (en-tête, pied de page, boutons) sont regroupés dans `app/views/mailers/shared/`. Les textes sont passés dans les fichiers de traduction (`config/locales/mailers.*.yml`).
- **Previews** : ajout de previews `ActionMailer::Preview` pour chaque email, disponibles sur `/rails/mailers` en développement.
- **Nettoyage** : suppression des callbacks `after_create :send_*_email` dans les modèles `User` et `Order`, et de la méthode utilitaire `EmailHelper.deliver_now_safe`, qui n'est plus utilisée.

### Impact

- Aucun changement fonctionnel attendu : les mêmes emails partent aux mêmes destinataires, avec le même contenu.
- Les emails ne bloquent plus la requête HTTP. Il faut donc qu'un worker Active Job (Sidekiq) traite la queue `mailers` en production.
- Création d'un utilisateur ou d'une commande en console ou dans un seed : plus aucun email n'est envoyé automatiquement. Il faut appeler le service correspondant explicitement.

### Tests

- Specs unitaires pour chaque service de notification (destinataires, conditions d'envoi, mise en queue).
- Specs de mailers : sujet, destinataires et présence des éléments clés dans le corps.
- Mise à jour des specs de requêtes avec `have_enqueued_mail` à la place de `ActionMailer::Base.deliveries`.
- Vérification manuelle de chaque email via les previews, en français et en anglais.

### Points d'attention pour la revue

- Vérifier qu'aucun envoi n'a été perdu lors de la suppression des callbacks : la liste complète est dans `spec/services/notifications/`.
- Vérifier la configuration de la queue `mailers` dans `config/sidekiq.yml` avant le déploiement.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
