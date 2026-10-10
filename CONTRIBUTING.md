# Contribuer à slopcheck-fr

Une règle entre dans un pack commun si elle repère un tic réel sans gêner la prose humaine. Le banc d'essai fournit la mesure, et chaque pull request l'affiche.

## Ajouter une règle

1. Écrivez la règle dans le pack visé (`src/slopcheck/packs/`), avec au moins un exemple `bad` et un exemple `good`. L'exemple `good` montre l'emploi légitime le plus proche : pour une règle sur le verbe plonger employé au figuré, une phrase où quelqu'un saute dans la Seine.
2. Lancez les tests :

   ```bash
   pip install -e .
   python -m unittest discover -s tests
   slopcheck test
   ```

3. Mesurez le taux sur le corpus humain avant votre ajout, puis après :

   ```bash
   slopcheck corpus fetch
   slopcheck bench --top 50
   ```

4. Collez les deux sorties dans la description de la pull request.

## Seuils d'admission

| Pack | BLOCK | WARN |
|---|---|---|
| `fr-signatures` | moins de 0,02 occurrence pour 1 000 mots humains | moins de 0,1 |
| `fr-strict` | le pack entier doit rester sous 1 BLOCK pour 1 000 mots | pas de seuil |
| `typo-fr` | aucune règle en BLOCK | pas de seuil |

Une règle trop bavarde peut entrer en WARN avec `escalate_at` : elle passe en BLOCK quand le texte la répète. Deux « véritable » dans un article relèvent du réflexe, un seul relève du choix.

## Choisir le bon outil

- Motif lexical ou syntaxique simple : une règle `regex`, avec `scope` (`block`, `sentence`, `first_sentence`, `last_sentence`, `title`, `raw`) et `unless` pour les exceptions.
- Liste de mots à compléter par les utilisateurs : une vérification intégrée avec `params` (voir `objet_agent`, `passive`, `lexical_density` dans `src/slopcheck/verifs.py`).
- Nouvelle vérification intégrée : une fonction dans `verifs.py`, enregistrée dans `CHECKS`, avec ses tests.

## Packs spécialisés

Un pack métier (juridique, académique, médical, marketing) vit dans son propre fichier et étend `fr-signatures`. Proposez-le dans `src/slopcheck/packs/` s'il sert à d'autres que vous ; gardez-le dans votre projet sinon. Un pack propre à une marque ou à une entreprise reste dans le dépôt de cette entreprise.

## Style des messages

Chaque règle porte un `message` (le problème, en une phrase) et un `fix` (la correction, avec un exemple si possible). Les deux passent slopcheck en mode strict.
