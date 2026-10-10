## Résumé

Cette pull request refactorise le module d’envoi d’e-mails afin d’améliorer sa lisibilité, sa maintenabilité et sa testabilité, sans modifier le comportement fonctionnel existant.

## Modifications principales

- Centralisation de la logique commune d’envoi.
- Séparation de la préparation des données et de l’expédition des e-mails.
- Simplification des mailers et suppression du code dupliqué.
- Harmonisation de la gestion des erreurs et des journaux.
- Clarification du nommage des classes et méthodes.
- Mise à jour des tests unitaires et d’intégration associés.

## Impact

Aucune modification n’est attendue pour les utilisateurs. Les modèles, destinataires et conditions d’envoi restent inchangés.

## Vérifications

- La suite de tests passe avec succès.
- Les principaux scénarios d’envoi ont été vérifiés.
- Les échecs d’expédition continuent d’être correctement journalisés et remontés.