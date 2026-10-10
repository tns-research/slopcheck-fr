## Correction de l'affichage des dates sur le tableau de bord

### Contexte

Sur le tableau de bord, certaines dates s'affichaient mal :

- Selon le fuseau horaire de l'utilisateur, les dates reçues de l'API au format ISO sans heure (`2026-10-09`) apparaissaient décalées d'un jour. `new Date()` les interprète en UTC, et l'affichage en heure locale reculait donc d'un jour.
- Le format n'était pas le même partout : `toLocaleDateString()` sans paramètre dans certains widgets, format codé en dur dans d'autres.
- Une valeur `null` ou invalide produisait « Invalid Date » au lieu d'un texte de remplacement.

### Modifications

- Nouvel utilitaire `formatDate` dans `src/utils/date.ts` :
  - il lit les dates sans heure comme des dates locales, ce qui supprime le décalage d'un jour ;
  - il formate avec `Intl.DateTimeFormat` selon la locale de l'utilisateur ;
  - il renvoie « — » pour une valeur absente ou invalide.
- Les composants `DashboardSummary`, `RecentActivity` et `StatsCard` utilisent désormais `formatDate` au lieu de leurs formatages locaux.
- Des tests unitaires couvrent les dates sans heure, les dates avec fuseau horaire, les valeurs nulles ou invalides et plusieurs locales (`fr-FR`, `en-US`).

### Comment tester

1. Lancer l'application avec `npm start` et ouvrir le tableau de bord.
2. Régler le fuseau horaire du système (ou du navigateur via les DevTools) sur une zone UTC négative, par exemple `America/New_York`.
3. Vérifier que les dates affichées correspondent à celles renvoyées par l'API.
4. Vérifier qu'une entrée sans date affiche « — ».
5. Lancer `npm test`.

### Impact

Seul l'affichage change. Les données et les appels à l'API restent identiques.
