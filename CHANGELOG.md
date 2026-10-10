# Changements

## 0.2.0 (9 octobre 2026)

Les règles ajoutées ou élargies visent dix familles de tics, choisies pour leur fréquence dans 224 textes générés par Claude et GPT-5.6 (`bench/genere-2026-10/`).

<!-- slopcheck: off -->
- Nouvelle règle `contraste-appose` : « X, et non Y », « X, pas Y » en fin de phrase. Remplace `apposition-pas` du pack strict.
- Nouvelle règle `emoji-tete` : émoji en tête de ligne, de puce ou d'intertitre. Les panneaux ⚠️, ℹ️ et ❗ restent en WARN.
- Nouvelles règles `hashtags` et `rituel-reseau` : bloc de hashtags, « la suite en commentaire », 👉, 👇, flèche en tête de ligne.
- Nouvelle règle `mot-gonfle` : « au cœur de », « niché », « authentique », « robuste », « levier », « incontournable »… en WARN dès une occurrence, en BLOCK à partir de trois.
- `puces-gras-serie` reconnaît `**Mot :**` et alerte dès trois puces d'affilée (BLOCK à cinq).
- `resultat-deux-points` relève « Résultat : » en tête de n'importe quelle phrase.
- `slopcheck bench` affiche le nombre de fichiers avec au moins un BLOCK et au moins une alerte.
- Corpus de 224 textes générés ajouté au dépôt, mesures à jour dans `docs/CALIBRAGE.md`.
- `--format github` échappe les annotations : un nom de fichier avec une virgule ou un deux-points cassait l'annotation.
- README refait, modèles d'issues (« Signaler un tic », « Faux positif »), `SECURITY.md`.
<!-- slopcheck: on -->

Pack par défaut sur la prose humaine : 0,14 BLOCK pour 1 000 mots (0,13 en 0.1.0). Textes générés relevés : 62 sur 224 avec au moins un BLOCK (31 en 0.1.0).

## 0.1.0

Première version : packs `fr-signatures`, `typo-fr`, `fr-strict`, commandes `check`, `rules`, `test`, `bench`, `learn`, `corpus`.
