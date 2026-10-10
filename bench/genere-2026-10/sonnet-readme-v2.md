# Panier Commun

Liste de courses partagée en temps réel entre colocataires. Ajoutez un article, cochez-le au rayon, et tout le monde voit la mise à jour tout de suite.

![Licence MIT](https://img.shields.io/badge/licence-MIT-green)
![Statut](https://img.shields.io/badge/statut-en%20développement-orange)

## Fonctionnalités

- **Listes partagées** : une ou plusieurs listes par colocation (courses, ménage, pharmacie…).
- **Synchronisation en temps réel** : les ajouts et les cases cochées apparaissent chez tous les colocataires sans recharger la page.
- **Qui achète quoi** : assignez un article à quelqu'un ou signalez « je m'en occupe ».
- **Catégories et rayons** : triez les articles par rayon pour faire les courses plus vite.
- **Articles récurrents** : programmez les basiques (lait, papier toilette, etc.).
- **Suivi des dépenses** (optionnel) : notez le montant du ticket et répartissez les frais.
- **Invitation par lien** : rejoignez une colocation sans créer de compte compliqué.
- **Mode hors ligne** : l'application fonctionne en PWA, même avec un réseau capricieux dans le supermarché.
- **Auto-hébergeable** : vos données restent chez vous.

## Installation

### Prérequis

- [Node.js](https://nodejs.org/) 20 ou supérieur
- [PostgreSQL](https://www.postgresql.org/) 15 ou supérieur (ou Docker)

### Avec Docker (recommandé)

```bash
git clone https://github.com/<votre-compte>/panier-commun.git
cd panier-commun
cp .env.example .env
docker compose up -d
```

L'application est accessible sur <http://localhost:3000>.

### Sans Docker

```bash
git clone https://github.com/<votre-compte>/panier-commun.git
cd panier-commun
cp .env.example .env
npm install
npm run db:migrate
npm run build
npm start
```

## Configuration

Les réglages se font dans le fichier `.env` :

| Variable | Description | Exemple |
|---|---|---|
| `DATABASE_URL` | Chaîne de connexion PostgreSQL | `postgres://user:mdp@localhost:5432/panier` |
| `SECRET_KEY` | Clé secrète pour les sessions (à générer) | `openssl rand -hex 32` |
| `BASE_URL` | URL publique de l'application | `https://courses.exemple.fr` |
| `PORT` | Port d'écoute | `3000` |
| `SMTP_URL` | Serveur d'envoi d'e-mails (optionnel) | `smtp://user:mdp@smtp.exemple.fr:587` |

## Développement

```bash
npm install
npm run dev        # serveur de développement avec rechargement à chaud
npm test           # tests unitaires et d'intégration
npm run lint       # vérification du style
```

## Structure du projet

```
panier-commun/
├── src/
│   ├── client/    # interface web
│   ├── server/    # API et temps réel
│   └── shared/    # types et utilitaires communs
├── migrations/    # migrations de base de données
├── docker-compose.yml
└── .env.example
```

## Contribuer

Les contributions sont les bienvenues, qu'il s'agisse d'un bug corrigé, d'une traduction ou d'une idée.

1. Forkez le dépôt.
2. Créez une branche : `git checkout -b ma-fonctionnalite`.
3. Commitez vos changements avec un message clair.
4. Vérifiez que `npm test` et `npm run lint` passent.
5. Ouvrez une *pull request* en décrivant ce qui change et pourquoi.

Pour un changement important, ouvrez d'abord une *issue* afin d'en discuter.

## Feuille de route

- [ ] Notifications push
- [ ] Scan de code-barres
- [ ] Import de tickets de caisse
- [ ] Application mobile native

## Licence

Distribué sous licence [MIT](LICENSE). Vous pouvez l'utiliser, la modifier et la redistribuer librement.
