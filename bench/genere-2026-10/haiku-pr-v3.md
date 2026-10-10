## Ajout de l'authentification à deux facteurs (2FA)

### Contexte
Les comptes adhérents donnent accès à des données de santé et de remboursement. Un mot de passe seul ne suffit plus à protéger ces données. Cette PR ajoute une étape de vérification en deux facteurs à la connexion.

### Changements
- Activation de la 2FA depuis l'espace adhérent, avec un QR code TOTP (application d'authentification) et une saisie de code de contrôle.
- Génération de codes de secours à usage unique, affichés une seule fois et stockés sous forme hachée.
- Nouvelle étape de vérification après la saisie du mot de passe, avec limitation des tentatives.
- Procédure de désactivation de la 2FA, protégée par une confirmation du mot de passe.
- Journalisation des événements liés à la 2FA (activation, désactivation, échecs répétés, utilisation d'un code de secours).

### Tests
- Tests unitaires sur la génération et la validation des codes TOTP, y compris la tolérance de décalage d'horloge.
- Tests d'intégration du parcours de connexion avec et sans 2FA.
- Tests de non-régression sur la récupération de mot de passe.

### Points d'attention
- Les secrets TOTP sont chiffrés au repos. La clé de chiffrement provient de la configuration d'environnement et doit être présente dans tous les environnements avant déploiement.
- Les adhérents qui perdent leur téléphone et leurs codes de secours devront passer par le support pour réinitialiser leur 2FA. Le parcours de support est à valider avec l'équipe adhésion.
- Migration : aucune contrainte pour les comptes existants, la 2FA reste facultative à ce stade.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
