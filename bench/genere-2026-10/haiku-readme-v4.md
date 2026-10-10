# Horaires d'Ouverture pour WordPress

Affiche les horaires d'ouverture de votre boutique sur la page d'accueil de votre site WordPress, avec mise en évidence de l'état en cours (ouvert ou fermé) et gestion des jours fériés et des fermetures exceptionnelles.

## Fonctionnalités

- Saisie des horaires par jour de la semaine, avec plusieurs créneaux possibles (par exemple matin et après-midi).
- Indicateur « Ouvert maintenant » ou « Fermé actuellement », mis à jour selon l'heure du serveur.
- Gestion des fermetures exceptionnelles (congés, jours fériés, travaux) avec un message personnalisé.
- Affichage automatique en haut ou en bas de la page d'accueil, ou placement manuel via un shortcode, un bloc Gutenberg ou une fonction PHP.
- Trois styles d'affichage fournis (liste, tableau, cartes), personnalisables via CSS.
- Traduction prête (fichiers `.pot` fournis, texte entièrement en français par défaut).
- Aucune dépendance externe, aucun script chargé sur les pages qui n'utilisent pas le plugin.

## Prérequis

- WordPress 6.0 ou supérieur
- PHP 7.4 ou supérieur

## Installation

1. Téléchargez l'archive `horaires-ouverture-boutique.zip` depuis la [page des versions](https://github.com/votre-compte/horaires-ouverture-boutique/releases).
2. Dans l'administration WordPress, allez dans **Extensions → Ajouter → Téléverser une extension**, puis sélectionnez l'archive.
3. Cliquez sur **Installer maintenant**, puis sur **Activer**.

Vous pouvez aussi copier le dossier dans `wp-content/plugins/` et l'activer depuis le menu **Extensions**.

## Configuration

1. Allez dans **Réglages → Horaires d'ouverture**.
2. Renseignez les horaires de chaque jour. Laissez un champ vide pour un jour de fermeture.
3. Pour ajouter un second créneau dans la journée, cliquez sur **+ Ajouter un créneau**.
4. Ajoutez les fermetures exceptionnelles dans la section dédiée, avec une date de début, une date de fin facultative et un motif.
5. Choisissez l'emplacement d'affichage et le style, puis enregistrez.

## Utilisation

### Affichage automatique sur la page d'accueil

Par défaut, le plugin insère le bloc en haut de la page d'accueil. Vous pouvez modifier cette position dans **Réglages → Horaires d'ouverture → Emplacement**.

### Shortcode

Insérez le shortcode suivant dans n'importe quelle page, article ou zone de widget :

```
[horaires_boutique style="tableau" afficher_statut="oui"]
```

| Attribut | Valeurs possibles | Défaut | Description |
|---|---|---|---|
| `style` | `liste`, `tableau`, `cartes` | `liste` | Présentation des horaires |
| `afficher_statut` | `oui`, `non` | `oui` | Affiche ou masque l'indicateur d'état |
| `jour_debut` | `lundi` à `dimanche` | `lundi` | Premier jour affiché |

### Fonction PHP

Pour l'intégrer dans un thème :

```php
<?php
if ( function_exists( 'horaires_boutique_afficher' ) ) {
	horaires_boutique_afficher( array( 'style' => 'cartes' ) );
}
```

### Bloc Gutenberg

Recherchez le bloc **Horaires d'ouverture** dans l'éditeur de blocs et insérez-le où vous le souhaitez.

## Personnalisation

Les styles utilisent des classes préfixées `hob-` et des variables CSS. Vous pouvez les surcharger dans le CSS de votre thème :

```css
.hob-horaires {
	--hob-couleur-ouvert: #2e7d32;
	--hob-couleur-ferme: #c62828;
	--hob-fond: #ffffff;
}
```

Des filtres sont également disponibles pour les développeurs :

- `hob_horaires_jours` : modifie la liste des jours avant affichage.
- `hob_est_ouvert` : force l'état ouvert ou fermé.
- `hob_message_fermeture` : personnalise le message affiché lors d'une fermeture exceptionnelle.

## Questions fréquentes

**Les horaires tiennent-ils compte du fuseau horaire ?**
Oui. Le plugin utilise le fuseau horaire défini dans **Réglages → Général** de WordPress.

**Le plugin ralentit-il mon site ?**
Non. Les horaires sont stockés dans une seule option WordPress et le CSS fait environ 2 Ko. Le calcul de l'état d'ouverture se fait côté PHP, sans requête supplémentaire.

**Puis-je afficher des horaires différents selon la langue ?**
Les horaires sont uniques pour le site. Pour un affichage multilingue, utilisez les noms de jours traduits par votre extension de traduction (WPML, Polylang).

**Le shortcode ne s'affiche pas correctement dans mon thème.**
Vérifiez que le style CSS du thème n'écrase pas les classes `hob-`. Vous pouvez aussi désactiver le CSS du plugin via le filtre `hob_charger_css` (retourner `false`).

## Contribuer

Les contributions sont les bienvenues.

1. Forkez le dépôt.
2. Créez une branche (`git checkout -b ma-fonctionnalite`).
3. Committez vos modifications et poussez la branche.
4. Ouvrez une Pull Request en décrivant le changement.

Merci de respecter les [standards de codage WordPress](https://developer.wordpress.org/coding-standards/) et de tester sur la dernière version stable de WordPress.

## Journal des modifications

### 1.0.0
- Première version publique.
- Saisie des horaires, fermetures exceptionnelles, shortcode, bloc Gutenberg et fonction PHP.

## Licence

Ce plugin est distribué sous licence [GPL v2 ou ultérieure](https://www.gnu.org/licenses/gpl-2.0.html), comme WordPress.

## Crédits

Développé par l'équipe du projet. Merci à tous les contributeurs.
