## Description

Cette pull request ajoute l’authentification à deux facteurs (2FA) afin de renforcer la sécurité des comptes adhérents.

### Changements apportés

- Activation et désactivation du 2FA depuis les paramètres de sécurité.
- Configuration via une application d’authentification compatible TOTP.
- Vérification du code à usage unique lors de la connexion.
- Génération de codes de récupération à usage unique.
- Gestion des erreurs, des codes expirés et des tentatives invalides.
- Mise à jour des écrans et messages associés au parcours d’authentification.
- Ajout de tests couvrant l’activation, la connexion, la récupération et la désactivation du 2FA.

### Sécurité et confidentialité

- Les secrets 2FA sont stockés de manière sécurisée.
- Les codes sensibles ne sont jamais consignés dans les journaux.
- Les données de santé et informations personnelles existantes ne sont pas modifiées.

### Vérification

1. Activer le 2FA depuis les paramètres du compte.
2. Scanner le QR code avec une application d’authentification.
3. Confirmer l’activation avec un code valide.
4. Se déconnecter, puis vérifier que le code 2FA est demandé à la prochaine connexion.
5. Tester un code invalide, un code expiré et un code de récupération.
6. Désactiver le 2FA et confirmer que la connexion classique reste fonctionnelle.