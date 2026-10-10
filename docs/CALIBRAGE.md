# Calibrage

Mesures du 9 octobre 2026, version 0.2.0. Commande : `slopcheck bench`, découpage en morceaux de 1 500 mots pour le corpus humain, sans découpage pour les textes générés.

## Corpus

- **Humain** : huit livres du domaine public (Voltaire, Dumas, Flaubert, Hugo, Proust, Zola, Verne, Descartes, 990 000 mots) et vingt articles de Wikipédia en français (245 000 mots). `slopcheck corpus fetch` les télécharge.
- **Généré, réglage** (`bench/ia/`) : huit textes écrits par Claude Sonnet sur des demandes ordinaires (article de blog, post LinkedIn, email de prospection, fiche produit, newsletter, guide, description d'événement, texte argumentatif), sans consigne de style. Six règles du pack `fr-signatures` viennent de la lecture de ces textes : `titre-conclusion`, `formule-toute-faite`, `cliche-sensoriel`, `et-vous`, `resultat-deux-points`, `annonce-reseau-social`.
- **Généré, contrôle** (`bench/ia-controle/`) : huit autres textes, mêmes conditions, sujets différents. Personne ne les a lus pour écrire des règles : ils mesurent la détection sur des textes que les règles n'ont jamais vus.
- **Généré, octobre 2026** (`bench/genere-2026-10/`) : 224 textes de Claude Haiku, Sonnet, Opus et GPT-5.6 sur quatorze genres, dont README, description de pull request, notes de version et documentation d'API. Détail des demandes dans `docs/CORPUS-GENERE.md`. Les règles ajoutées en 0.2.0 ont été réglées sur ce corpus.
- **README humains** : 45 README français de dépôts GitHub créés avant mi-2021, pour vérifier que les règles de mise en forme ne visent pas la documentation technique ordinaire. Ils ne sont pas redistribués dans le dépôt.

## Résultats

BLOCK pour 1 000 mots :

| Corpus | Mots | `fr-signatures` + `typo-fr` (défaut) | `fr-strict` |
|---|---|---|---|
| Livres du domaine public | 990 000 | 0,12 | 0,86 |
| Wikipédia | 244 853 | 0,19 | 0,95 |
| README humains (avant 2021) | 24 416 | 0,16 | |
| Textes générés, réglage | 2 924 | 16,07 | 20,86 |
| Textes générés, contrôle | 3 027 | 4,96 | 9,25 |
| Textes générés, octobre 2026 (hors `placeholder`) | 60 575 | 2,03 | 3,93 |

Textes qui lèvent au moins un BLOCK, pack par défaut :

| Corpus | 0.1.0 | 0.2.0 |
|---|---|---|
| Contrôle (8 textes jamais lus) | 3 | 6 |
| Octobre 2026 (224 textes, hors `placeholder`) | 31 | 62 |
| Octobre 2026, au moins une alerte BLOCK ou WARN | 84 | 130 |
| README humains (45) | 4 | 4 |

La règle `placeholder` est retirée de ce décompte : les demandes ne donnaient ni nom ni lien, et les modèles ont laissé des `[lien]`. Ce cas ne dit rien des tics.

94 des 224 textes générés sortent encore sans aucune alerte : 15 lettres de motivation sur 16, 13 avis clients sur 16, 11 emails sur 16, 10 discours sur 16, et la moitié des textes techniques (README, documentation d'API, notes de version, pull requests). Ces textes sont plats et corrects. Ils n'ont pas de tic de surface, et un détecteur à règles ne voit que la surface. C'est la raison de `slopcheck learn` : chaque utilisateur ajoute les tournures qu'il repère dans ses propres textes.

## Règles les plus bavardes sur la prose humaine

Pack par défaut, pour 1 000 mots :

| Règle | BLOCK | WARN | Source principale |
|---|---|---|---|
| `em-dash` | 0,066 | 0,100 | incises au tiret chez Dumas et Hugo |
| `veritable` | 0,021 | 0,091 | « véritable » en intensificateur, fréquent au XIXe siècle |
| `correction-deux-temps` | 0,022 | | dialogues où un personnage en désigne un autre |
| `fausse-revelation` | 0,008 | | interjections de dialogue chez Dumas et Hugo |
| `mot-gonfle` | 0,007 | 0,092 | « exceptionnel », « au cœur de » dans les romans et les articles de géographie |
| `contraste-appose` | | 0,023 | « et non pas » chez Descartes, Dumas et Voltaire |
| `espace-ponctuation` | | 1,53 | transcriptions Gutenberg sans espace avant « ; » |

## Reproduire

```bash
slopcheck corpus fetch
slopcheck bench
slopcheck bench --strict
slopcheck bench --chunk 0 bench/ia bench/ia-controle
printf 'disable = ["placeholder"]\n' > /tmp/sans-placeholder.toml
slopcheck bench --chunk 0 --config /tmp/sans-placeholder.toml bench/genere-2026-10
```
