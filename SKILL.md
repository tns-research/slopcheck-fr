---
name: slopcheck-fr
description: Vérifie un texte français avant livraison et corrige les tics d'écriture IA (faux contrastes « ce n'est pas X, c'est Y » ou « X, pas Y », puces en gras, émojis en tête de ligne, hashtags, mots gonflés, tirets cadratins, plan scolaire, fausses révélations, typographie anglaise). À lancer sur tout texte en français destiné à être lu (post, email, article, README, page, fiche produit, newsletter) avant de le rendre. Déterministe, sans appel réseau.
compatibility: Python 3.11+, commande slopcheck installée (pip install git+https://github.com/tns-research/slopcheck-fr)
---

## Boucle de livraison

1. Écrire le texte dans un fichier.
2. Lancer `slopcheck --format json <fichier>` (ajouter `--strict` si l'utilisateur veut une prose sèche et factuelle).
3. Corriger chaque constat `block` en suivant son champ `fix`. Supprimer la tournure vaut souvent mieux que la reformuler.
4. Relire chaque constat `warn` : corriger, ou garder si la tournure est un choix justifiable.
5. Relancer jusqu'à zéro `block`.
6. Relire le fond, que les règles ne voient pas. Un texte sans alerte peut rester plat : chaque paragraphe doit porter au moins un fait précis (chiffre, nom, date, exemple) ou un avis tranché. Signaler à l'utilisateur les paragraphes qui n'en ont pas plutôt que d'inventer le fait.
7. Livrer.

## Règles de correction

- Ne pas ajouter de fait, de chiffre ou de source absents du brief pour combler un trou. Signaler le manque à l'utilisateur.
- Ne pas contourner une règle par un synonyme : remplacer un intensificateur par un autre ne corrige rien. Supprimer le mot, ou écrire le fait mesuré.
- Un tiret cadratin se remplace par une virgule, des parenthèses, un deux-points ou un point. Jamais par un double trait d'union.
- `<!-- slopcheck: ignore code -->` sert seulement aux citations et aux exemples, jamais à faire passer son propre texte.

## Apprendre de l'utilisateur

Quand l'utilisateur rejette une tournure, proposer de l'ajouter à son pack :

```bash
slopcheck learn "la tournure rejetée" --save slopcheck-perso.toml
```

Montrer le verdict de la commande (occurrences sur le corpus humain, sévérité conseillée) avant d'enregistrer.
