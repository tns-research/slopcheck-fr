## Correction : affichage des dates sur le tableau de bord

### Contexte
Les dates affichées sur le tableau de bord étaient incorrectes pour certains utilisateurs : décalage d'un jour selon le fuseau horaire, et formats non conformes à la locale française.

### Cause
Les dates étaient converties avec `new Date(...)` puis formatées en UTC, ce qui décale l'affichage pour les fuseaux éloignés d'UTC. Le formatage ne tenait pas compte de la locale de l'utilisateur.

### Modifications
- Remplacement de la mise en forme manuelle par `Intl.DateTimeFormat` avec la locale `fr-FR`.
- Conversion des dates au fuseau horaire de l'utilisateur avant l'affichage, sans modifier les valeurs stockées.
- Ajout de tests unitaires couvrant les fuseaux horaires proches de minuit et les dates en fin de mois.

### Tests
- [ ] Tests unitaires passants
- [ ] Vérification manuelle sur le tableau de bord avec plusieurs fuseaux horaires (Paris, New York, Tokyo)
- [ ] Vérification du rendu sur les cartes de statistiques et le graphique d'activité

🤖 Generated with [Claude Code](https://claude.com/claude-code)
