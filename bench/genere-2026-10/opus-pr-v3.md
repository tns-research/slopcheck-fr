## Ajout de l'authentification à deux facteurs (2FA) sur l'espace adhérent

### Contexte

L'espace adhérent donne accès à des données de santé : remboursements, décomptes, attestations et prises en charge hospitalières. Ces données sont sensibles au sens de l'article 9 du RGPD. Une authentification par mot de passe seul n'est plus suffisante, comme le rappellent les recommandations de l'ANSSI et de la CNIL.

Cette PR ajoute une authentification à deux facteurs pour les adhérents et la rend obligatoire pour les comptes gestionnaires du back-office.

### Changements

**Parcours adhérent**
- Activation de la 2FA depuis « Mon compte > Sécurité », avec deux méthodes au choix :
  - une application d'authentification (TOTP, RFC 6238) comme Google Authenticator, Microsoft Authenticator ou FreeOTP ;
  - un code à usage unique envoyé par e-mail, en solution de repli.
- 10 codes de secours générés à l'activation. Ils ne s'affichent qu'une fois et peuvent être téléchargés ou imprimés.
- Option « Faire confiance à cet appareil pendant 30 jours », grâce à un cookie signé, `HttpOnly`, `Secure` et `SameSite=Strict`.
- Second facteur redemandé pour les actions sensibles, même sur un appareil de confiance : modification du RIB, de l'adresse e-mail ou du mot de passe, et désactivation de la 2FA.

**Back-office**
- 2FA TOTP obligatoire pour tous les comptes gestionnaires. Le compte est bloqué tant que l'enrôlement n'est pas terminé.
- Nouvel écran de support pour réinitialiser la 2FA d'un adhérent après vérification de son identité. L'action est tracée dans le journal d'audit.

**Sécurité**
- Secrets TOTP chiffrés au repos (AES-256-GCM) avec une clé gérée par le KMS, jamais stockés en clair.
- Codes de secours hachés avec Argon2id et invalidés après usage.
- Fenêtre de tolérance TOTP de ±1 pas (30 s), avec protection contre le rejeu d'un code déjà utilisé.
- Limitation des tentatives : 5 échecs entraînent un blocage temporaire de 15 minutes, puis une notification par e-mail à l'adhérent.
- Codes e-mail valables 10 minutes, à usage unique.
- Événements journalisés sans donnée sensible : activation, désactivation, échec, utilisation d'un code de secours, réinitialisation par le support.
- Notification par e-mail à chaque activation ou désactivation de la 2FA.

**Technique**
- Migration : nouvelles tables `user_mfa_methods`, `user_mfa_recovery_codes` et `trusted_devices`.
- Nouveau middleware `RequireMfa` appliqué aux routes de l'espace adhérent et du back-office.
- Feature flag `mfa_adherents` pour un déploiement progressif côté adhérents.
- Pages accessibles (RGAA) : champs de code compatibles avec la saisie automatique (`autocomplete="one-time-code"`), messages d'erreur annoncés aux lecteurs d'écran, et QR code accompagné de la clé en texte.

### Tests

- Tests unitaires : génération et vérification TOTP, rejeu, expiration des codes e-mail, codes de secours, limitation des tentatives.
- Tests d'intégration : connexion avec et sans 2FA, appareil de confiance, actions sensibles, réinitialisation par le support.
- Tests end-to-end (Playwright) : enrôlement complet et connexion avec un code de secours.
- Recette manuelle avec les principales applications d'authentification sur iOS et Android.

### Déploiement

1. Lancer la migration (rétrocompatible, sans interruption de service).
2. Déployer avec `mfa_adherents` désactivé. La 2FA est immédiatement obligatoire pour le back-office.
3. Activer le flag pour un panel d'adhérents, puis pour tous, après validation par le support.
4. Le support client a reçu une fiche de procédure pour les demandes de réinitialisation.

### Points d'attention pour la revue

- Durée de confiance d'un appareil (30 jours) à valider avec le RSSI.
- La méthode par SMS est volontairement exclue (risque de SIM swapping). Elle pourra être réexaminée plus tard si le besoin est confirmé.
- Le DPO doit valider la mise à jour de la politique de confidentialité, car de nouvelles données sont traitées (appareils de confiance et journaux de connexion).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
