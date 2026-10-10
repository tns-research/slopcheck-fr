# Coloccourses

Une liste de courses partagée en temps réel, pensée pour les colocataires. Chacun ajoute ce qui manque, coche ce qu'il a acheté, et tout le monde voit la même liste.

## Fonctionnalités

- **Liste partagée** : tous les membres d'un logement voient la même liste, mise à jour en temps réel.
- **Ajout rapide** : saisie d'un article en une ligne, avec quantité et catégorie facultatives.
- **Cocher / décocher** : marquer un article comme acheté, avec le nom de la personne qui l'a coché.
- **Catégories** : regroupement automatique par rayon (fruits et légumes, épicerie, hygiène, entretien…).
- **Historique** : retrouver les articles achetés récemment pour les racheter en un clic.
- **Groupes de colocation** : créer un logement, inviter ses colocataires par lien, gérer les membres.
- **Responsive** : utilisable sur mobile, en magasin comme sur ordinateur.
- **Open source** : code libre, auto-hébergeable sur votre propre serveur.

## Captures d'écran

> *À compléter : ajoutez vos captures dans `docs/screenshots/`.*

## Stack technique

- **Backend** : Node.js, Express
- **Base de données** : SQLite (via better-sqlite3)
- **Temps réel** : Server-Sent Events
- **Frontend** : HTML, CSS et JavaScript, sans framework lourd
- **Tests** : Vitest

## Prérequis

- Node.js 20 ou supérieur
- npm 10 ou supérieur

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/<votre-compte>/colocourses.git
cd colocourses

# Installer les dépendances
npm install

# Copier le fichier de configuration
cp .env.example .env

# Lancer l'application en développement
npm run dev
```

L'application est ensuite accessible sur [http://localhost:3000](http://localhost:3000).

## Configuration

Les variables d'environnement sont définies dans le fichier `.env` :

| Variable         | Description                                          | Valeur par défaut         |
| ---------------- | ---------------------------------------------------- | ------------------------- |
| `PORT`           | Port d'écoute du serveur                             | `3000`                    |
| `DATABASE_PATH`  | Chemin du fichier SQLite                             | `./data/colocourses.db`   |
| `SESSION_SECRET` | Clé secrète pour les sessions (à changer en production) | *aucune*               |
| `INVITE_TTL_H`   | Durée de validité d'un lien d'invitation, en heures  | `72`                      |

> Générez une clé robuste avec `openssl rand -hex 32`.

## Utilisation

1. Créez un compte, puis un logement (par exemple « 12 rue des Lilas »).
2. Partagez le lien d'invitation généré avec vos colocataires.
3. Ajoutez les articles dans la liste ; chacun peut les cocher au magasin.
4. Une fois la course terminée, utilisez **Vider les articles cochés** pour repartir sur une liste propre.

## Scripts disponibles

| Commande           | Action                                      |
| ------------------ | ------------------------------------------- |
| `npm run dev`      | Lance le serveur en mode développement      |
| `npm start`        | Lance le serveur en production              |
| `npm test`         | Exécute les tests unitaires et d'intégration |
| `npm run lint`     | Vérifie le style du code                    |

## Déploiement

Un exemple de déploiement avec Docker est fourni :

```bash
docker compose up -d
```

Le volume `./data` contient la base de données : pensez à le sauvegarder régulièrement.

## Structure du projet

```
colocourses/
├── src/
│   ├── server.js        # Point d'entrée du serveur
│   ├── routes/          # Routes de l'API
│   ├── db/              # Schéma et accès à SQLite
│   └── realtime.js      # Diffusion des mises à jour (SSE)
├── public/              # Interface web (HTML, CSS, JS)
├── tests/               # Tests
├── docs/                # Documentation et captures
└── docker-compose.yml
```

## Contribuer

Les contributions sont les bienvenues.

1. Forkez le dépôt et créez une branche : `git checkout -b ma-fonctionnalite`
2. Faites vos modifications et ajoutez des tests si possible.
3. Vérifiez que `npm test` et `npm run lint` passent.
4. Ouvrez une Pull Request en décrivant clairement le changement.

Pour signaler un bug ou proposer une idée, ouvrez une [issue](https://github.com/<votre-compte>/colocourses/issues).

## Licence

Distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
