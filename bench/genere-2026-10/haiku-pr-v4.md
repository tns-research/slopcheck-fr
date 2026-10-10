## Refactorisation du module d'envoi d'emails

### Contexte

La logique d'envoi d'emails était dispersée entre les mailers, les contrôleurs et plusieurs callbacks de modèles. Cela rendait les envois difficiles à tester, à suivre et à modifier sans effets de bord.

### Changements

- Extraction de la logique d'envoi dans un service dédié (`EmailDispatcher`), qui est le seul point d'entrée pour envoyer un email.
- Les mailers ne contiennent plus que la construction du message (destinataire, objet, corps).
- Suppression des appels d'envoi directs dans les contrôleurs et les callbacks `after_*` des modèles, remplacés par des appels au service.
- Centralisation des règles communes (expéditeur par défaut, gestion des emails désabonnés, journalisation des erreurs) dans le service.
- Ajout de tests unitaires sur le service et de tests de non-régression sur les parcours qui déclenchent un email.

### Notes pour la review

- Aucun changement de comportement attendu côté utilisateur : les objets, les destinataires et les templates sont inchangés.
- Les envois sont désormais explicites. Un email qui n'était pas envoyé avant ne doit pas apparaître après cette PR. Merci de vérifier les parcours d'inscription et de réinitialisation de mot de passe en priorité.
- Les jobs d'envoi (`deliver_later`) sont conservés. Seule leur invocation a été déplacée.

### Tests

- `bundle exec rspec spec/services/email_dispatcher_spec.rb spec/mailers spec/requests`
- Test manuel en environnement de staging sur l'inscription, la réinitialisation du mot de passe et la confirmation de commande.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
