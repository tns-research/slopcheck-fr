# Courses en Coloc

Application web open source permettant aux colocataires de créer, partager et gérer une liste de courses commune en temps réel.

## Fonctionnalités

- Création de colocations privées
- Liste de courses partagée
- Ajout, modification et suppression d’articles
- Classement par catégories
- Attribution d’articles à un colocataire
- Synchronisation en temps réel
- Historique des achats
- Interface responsive
- Mode sombre
- Invitations par lien

## Installation

### Prérequis

- Node.js 20 ou supérieur
- npm 10 ou supérieur

### Démarrage local

```bash
git clone https://github.com/votre-utilisateur/courses-en-coloc.git
cd courses-en-coloc
npm install
cp .env.example .env
npm run dev
```

L’application est ensuite accessible sur [http://localhost:3000](http://localhost:3000).

## Configuration

Créez un fichier `.env` à partir de `.env.example`, puis renseignez les variables nécessaires :

```env
DATABASE_URL=
AUTH_SECRET=
APP_URL=http://localhost:3000
```

Ne publiez jamais vos secrets dans le dépôt.

## Scripts

```bash
npm run dev       # Lance le serveur de développement
npm run build     # Génère la version de production
npm run start     # Lance la version de production
npm run lint      # Analyse le code
npm run test      # Exécute les tests
```

## Utilisation

1. Créez un compte.
2. Créez une colocation ou rejoignez-en une avec un lien d’invitation.
3. Ajoutez les produits nécessaires à la liste commune.
4. Cochez les articles placés dans le panier.
5. Consultez l’historique pour suivre les achats précédents.

## Contribution

Les contributions sont les bienvenues.

1. Forkez le dépôt.
2. Créez une branche :

```bash
git checkout -b feature/ma-fonctionnalite
```

3. Effectuez vos modifications et ajoutez les tests nécessaires.
4. Vérifiez le projet :

```bash
npm run lint
npm run test
```

5. Ouvrez une pull request en décrivant clairement vos changements.

Consultez également le fichier [`CONTRIBUTING.md`](CONTRIBUTING.md) avant de contribuer.

## Signaler un problème

Avant d’ouvrir une issue, vérifiez qu’un problème similaire n’existe pas déjà. Précisez autant que possible :

- les étapes permettant de reproduire le problème ;
- le comportement attendu ;
- le comportement observé ;
- votre navigateur et votre système d’exploitation ;
- les captures d’écran ou messages d’erreur utiles.

## Sécurité

Pour signaler une vulnérabilité, évitez de créer une issue publique. Suivez les instructions du fichier [`SECURITY.md`](SECURITY.md).

## Licence

Ce projet est distribué sous licence MIT. Consultez le fichier [`LICENSE`](LICENSE) pour plus d’informations.