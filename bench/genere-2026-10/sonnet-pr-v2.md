## Correction de l'affichage des dates sur le tableau de bord

### Contexte

Sur le tableau de bord, certaines dates s'affichaient avec un jour de décalage ou dans un format incohérent (par exemple `2026-10-09` au lieu de `09/10/2026`). Le problème venait de la conversion des dates ISO via `new Date()`, qui les interprétait en UTC puis les affichait dans le fuseau horaire local du navigateur. Le format dépendait en outre de la locale par défaut du navigateur.

### Changements

- Ajout d'un utilitaire `formatDate` centralisé, qui utilise `Intl.DateTimeFormat` avec la locale `fr-FR` et un fuseau horaire explicite.
- Remplacement des appels à `toLocaleDateString()` et des formatages manuels dans les composants `DashboardHeader`, `ActivityList` et `StatsCard`.
- Gestion des valeurs `null`, `undefined` et des dates invalides : affichage de `–` au lieu de `Invalid Date`.
- Ajout de tests unitaires couvrant les changements de fuseau horaire, le passage à l'heure d'été et les dates invalides.

### Comment tester

1. Lancer l'application et ouvrir le tableau de bord.
2. Vérifier que les dates s'affichent au format `JJ/MM/AAAA`.
3. Changer le fuseau horaire du navigateur (par exemple UTC−8 puis UTC+10) et vérifier que les dates restent identiques.
4. Exécuter `npm test` : tous les tests doivent passer.

### Captures d'écran

| Avant | Après |
|-------|-------|
| _à ajouter_ | _à ajouter_ |

### Notes

Aucun changement d'API ni de schéma de données. Les autres pages utilisent encore leur propre formatage et pourront migrer vers `formatDate` dans une PR ultérieure.
