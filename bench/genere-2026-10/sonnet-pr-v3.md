## Ajout de l'authentification à deux facteurs (2FA) sur l'espace adhérent

### Contexte

L'espace adhérent donne accès à des données de santé (remboursements, décomptes, attestations) et à des données bancaires (RIB). Un mot de passe seul ne suffit plus à les protéger. Cette PR ajoute une seconde étape de vérification à la connexion, pour limiter les risques de prise de contrôle de compte (réutilisation de mots de passe, hameçonnage).

### Ce qui change

- **Activation facultative** depuis *Mon profil > Sécurité*. L'adhérent choisit sa méthode :
  - application d'authentification (TOTP, compatible Google Authenticator, Authy, etc.) ;
  - code à usage unique envoyé par SMS.
- **Étape de vérification à la connexion** après la saisie correcte de l'identifiant et du mot de passe.
- **Codes de secours** : 10 codes à usage unique générés à l'activation, affichés une seule fois et stockés hachés.
- **Option « Faire confiance à cet appareil pendant 30 jours »** via un cookie signé, `HttpOnly` et `Secure`.
- **Désactivation et régénération des codes de secours** soumises à une nouvelle saisie du mot de passe et d'un code 2FA.
- **Notifications par e-mail** à l'activation, à la désactivation et à l'utilisation d'un code de secours.
- **Parcours de récupération** en cas de perte de l'appareil, via une vérification d'identité par le support (voir la procédure ajoutée à la documentation interne).

### Choix techniques

- Secrets TOTP chiffrés au repos (AES-256-GCM), la clé étant gérée par le gestionnaire de secrets existant.
- Tolérance de dérive horaire de ±1 intervalle de 30 secondes.
- Codes SMS valables 5 minutes, à usage unique.
- Limitation du nombre de tentatives : 5 essais, puis blocage temporaire de 15 minutes avec journalisation.
- Comparaison des codes en temps constant.
- Aucune donnée de santé ni information sensible dans les journaux ou les messages SMS.
- Migration de base de données additive uniquement (nouvelle table `user_mfa` et colonnes de suivi), sans impact sur les comptes existants.

### Protection des données (RGPD)

- Le numéro de téléphone n'est collecté que si l'adhérent choisit la méthode SMS. Il sert uniquement à l'authentification.
- Mention ajoutée dans la politique de confidentialité et dans le registre des traitements (à valider par le DPO avant mise en production).
- Les journaux d'authentification sont conservés 12 mois.

### Accessibilité

- Champs de saisie libellés et compatibles lecteur d'écran.
- Saisie du code possible par copier-coller et par remplissage automatique.
- Messages d'erreur explicites, sans dépendre uniquement de la couleur.

### Tests

- Tests unitaires : génération et validation TOTP, expiration des codes SMS, usage unique des codes de secours, verrouillage après échecs.
- Tests d'intégration : activation, connexion avec 2FA, appareil de confiance, désactivation, récupération.
- Test manuel sur iOS et Android avec deux applications d'authentification différentes.
- Couverture du nouveau module : 94 %.

### Déploiement

- Fonctionnalité derrière le drapeau `FEATURE_2FA_ENABLED`, désactivé par défaut.
- Déploiement progressif : interne, puis 10 % des adhérents, puis généralisation.
- Retour arrière : désactiver le drapeau, sans migration inverse nécessaire.
- Prévenir le support avant l'activation (FAQ et procédure de récupération fournies).

### À vérifier en relecture

- [ ] Gestion de la clé de chiffrement des secrets TOTP
- [ ] Paramètres de limitation des tentatives
- [ ] Textes des e-mails et SMS
- [ ] Validation du DPO sur la mention RGPD

### Suite prévue (hors périmètre de cette PR)

- Rendre la 2FA obligatoire pour les comptes gestionnaires et les conseillers
- Prise en charge des clés de sécurité (WebAuthn / passkeys)
