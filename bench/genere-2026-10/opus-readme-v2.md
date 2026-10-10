# 🛒 Panier Commun

**La liste de courses partagée de votre colocation.** Panier Commun est une application web open source qui permet aux colocataires de tenir une liste de courses commune, synchronisée en temps réel, et de répartir les dépenses sans prise de tête.

[![Licence : AGPL-3.0](https://img.shields.io/badge/licence-AGPL--3.0-blue.svg)](LICENSE)
[![CI](https://github.com/votre-organisation/panier-commun/actions/workflows/ci.yml/badge.svg)](https://github.com/votre-organisation/panier-commun/actions)
[![Contributions bienvenues](https://img.shields.io/badge/contributions-bienvenues-brightgreen.svg)](CONTRIBUTING.md)

---

## Sommaire

- [Fonctionnalités](#fonctionnalités)
- [Aperçu](#aperçu)
- [Stack technique](#stack-technique)
- [Installation rapide avec Docker](#installation-rapide-avec-docker)
- [Installation pour le développement](#installation-pour-le-développement)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Tests](#tests)
- [Feuille de route](#feuille-de-route)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## Fonctionnalités

- **Listes partagées en temps réel** : un article ajouté par un colocataire apparaît aussitôt chez tous les autres.
- **Foyers et invitations** : créez votre coloc et invitez les autres par lien ou par code.
- **Catégories et rayons** : les articles sont classés automatiquement (frais, épicerie, hygiène, entretien…) pour faire les courses plus vite en magasin.
- **Mode courses** : cochez les articles au fur et à mesure, même hors connexion. La synchronisation se fait au retour du réseau.
- **Articles récurrents** : papier toilette, lait, café… ajoutez-les à la liste en un clic.
- **Partage des dépenses** : saisissez le montant du ticket, choisissez qui participe, et l'application calcule qui doit combien à qui.
- **Historique** : retrouvez les courses passées et les dépenses du mois.
- **Notifications** : soyez prévenu quand quelqu'un part faire les courses ou ajoute un article urgent.
- **Application installable (PWA)** : fonctionne sur mobile comme une application native, sans passer par un store.
- **Auto-hébergeable** : vos données restent chez vous.

## Aperçu

| Liste partagée | Mode courses | Dépenses |
| :---: | :---: | :---: |
| ![Liste partagée](docs/captures/liste.png) | ![Mode courses](docs/captures/mode-courses.png) | ![Dépenses](docs/captures/depenses.png) |

## Stack technique

| Couche | Technologies |
| --- | --- |
| Front-end | React, TypeScript, Vite, Tailwind CSS |
| Back-end | Node.js, Fastify, TypeScript |
| Temps réel | WebSocket (Socket.IO) |
| Base de données | PostgreSQL, Prisma |
| Hors ligne | Service Worker, IndexedDB |
| Déploiement | Docker, Docker Compose |

## Installation rapide avec Docker

Prérequis : [Docker](https://docs.docker.com/get-docker/) et Docker Compose.

```bash
git clone https://github.com/votre-organisation/panier-commun.git
cd panier-commun
cp .env.example .env
docker compose up -d
```

L'application est ensuite accessible sur [http://localhost:8080](http://localhost:8080).

> Pensez à modifier `JWT_SECRET` et les identifiants de la base de données dans `.env` avant toute mise en production.

## Installation pour le développement

Prérequis :

- Node.js 20 ou plus récent
- pnpm 9 ou plus récent
- PostgreSQL 15 ou plus récent (ou `docker compose up -d db`)

```bash
# Cloner le dépôt
git clone https://github.com/votre-organisation/panier-commun.git
cd panier-commun

# Installer les dépendances
pnpm install

# Configurer l'environnement
cp .env.example .env

# Appliquer les migrations et charger des données de démonstration
pnpm db:migrate
pnpm db:seed

# Lancer le front et le back en mode développement
pnpm dev
```

- Front-end : [http://localhost:5173](http://localhost:5173)
- API : [http://localhost:3000](http://localhost:3000)

Les données de démonstration créent une colocation « Rue des Lilas » avec trois comptes (`alice@exemple.fr`, `bastien@exemple.fr`, `chloe@exemple.fr`), mot de passe `motdepasse`.

## Configuration

Les variables d'environnement se définissent dans le fichier `.env` :

| Variable | Description | Valeur par défaut |
| --- | --- | --- |
| `DATABASE_URL` | URL de connexion PostgreSQL | `postgresql://panier:panier@localhost:5432/panier` |
| `JWT_SECRET` | Clé de signature des jetons d'authentification | *(obligatoire)* |
| `APP_URL` | URL publique de l'application, utilisée dans les liens d'invitation | `http://localhost:8080` |
| `PORT` | Port de l'API | `3000` |
| `SMTP_URL` | Serveur SMTP pour les e-mails d'invitation (facultatif) | *(vide)* |
| `VAPID_PUBLIC_KEY` / `VAPID_PRIVATE_KEY` | Clés pour les notifications push (facultatif) | *(vide)* |
| `DEFAULT_CURRENCY` | Devise par défaut des dépenses | `EUR` |

Pour générer les clés VAPID :

```bash
pnpm generate:vapid
```

## Utilisation

1. **Créez un compte**, puis une colocation.
2. **Invitez vos colocataires** en partageant le lien d'invitation ou le code à six caractères.
3. **Ajoutez des articles** à la liste. La quantité et une note (« la marque bio », « pas plus de 3 € ») sont facultatives.
4. **Au magasin**, activez le mode courses et cochez ce que vous mettez dans le panier.
5. **À la caisse**, saisissez le montant du ticket et choisissez les participants. Les soldes de chacun sont mis à jour automatiquement.
6. **Pour régler les comptes**, l'onglet « Soldes » propose le nombre minimal de remboursements pour revenir à zéro.

## Structure du projet

```
panier-commun/
├── apps/
│   ├── web/            # Front-end React (PWA)
│   └── api/            # API Fastify et serveur WebSocket
├── packages/
│   ├── shared/         # Types et schémas de validation partagés
│   └── ui/             # Composants d'interface réutilisables
├── prisma/             # Schéma et migrations de la base
├── docs/               # Documentation et captures d'écran
├── docker-compose.yml
└── .env.example
```

## Tests

```bash
pnpm test          # Tests unitaires
pnpm test:e2e      # Tests de bout en bout (Playwright)
pnpm lint          # Analyse statique
pnpm typecheck     # Vérification des types
```

## Feuille de route

- [x] Listes partagées en temps réel
- [x] Mode hors ligne
- [x] Partage des dépenses
- [ ] Scan des tickets de caisse (OCR)
- [ ] Plusieurs listes par colocation (courses, bricolage, pharmacie…)
- [ ] Export des dépenses en CSV
- [ ] Traductions (anglais, espagnol, allemand)
- [ ] Planning des tâches ménagères

Les idées et demandes de fonctionnalités se discutent dans les [issues](https://github.com/votre-organisation/panier-commun/issues).

## Contribuer

Les contributions sont les bienvenues, qu'il s'agisse de code, de traductions, de design ou de signalements de bugs.

1. Forkez le dépôt.
2. Créez une branche : `git checkout -b feature/ma-fonctionnalite`.
3. Commitez vos modifications en suivant les [Conventional Commits](https://www.conventionalcommits.org/fr/).
4. Vérifiez que les tests passent : `pnpm test && pnpm lint`.
5. Ouvrez une pull request en décrivant ce que vous avez changé et pourquoi.

Avant de contribuer, merci de lire le [guide de contribution](CONTRIBUTING.md) et le [code de conduite](CODE_OF_CONDUCT.md).

Pour signaler une faille de sécurité, n'ouvrez pas d'issue publique : écrivez plutôt à l'adresse indiquée dans [SECURITY.md](SECURITY.md).

## Licence

Panier Commun est distribué sous licence [GNU AGPL-3.0](LICENSE). Vous pouvez l'utiliser, le modifier et l'héberger librement. Si vous proposez une version modifiée en tant que service en ligne, vous devez en publier le code source.

---

Fait avec ❤️ par des colocataires fatigués de racheter trois fois du sel.
