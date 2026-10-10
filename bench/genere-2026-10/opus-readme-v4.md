# Horaires Boutique

Plugin WordPress qui affiche les horaires d'ouverture de votre boutique sur la page d'accueil. Il indique aussi en temps réel si la boutique est ouverte ou fermée.

![Licence GPL v2](https://img.shields.io/badge/licence-GPLv2%2B-blue.svg)
![WordPress 6.0+](https://img.shields.io/badge/WordPress-6.0%2B-21759b.svg)
![PHP 7.4+](https://img.shields.io/badge/PHP-7.4%2B-777bb4.svg)

## Fonctionnalités

- Horaires réglables jour par jour, avec plusieurs plages possibles dans une journée (par exemple 9 h-12 h 30 et 14 h-19 h)
- Affichage automatique sur la page d'accueil, sans toucher au thème
- Indicateur « Ouvert maintenant » / « Fermé », calculé selon le fuseau horaire du site
- Fermetures exceptionnelles et jours fériés, avec un message personnalisé
- Trois formats d'affichage : tableau, liste ou ligne compacte
- Shortcode, bloc Gutenberg et widget pour afficher les horaires ailleurs sur le site
- Balisage Schema.org (`OpeningHoursSpecification`) pour le référencement local
- Prêt pour la traduction (fichier `.pot` fourni)

## Prérequis

- WordPress 6.0 ou plus récent
- PHP 7.4 ou plus récent

## Installation

### Depuis l'administration WordPress

1. Téléchargez la dernière version (`horaires-boutique.zip`) depuis la page [Releases](https://github.com/votre-compte/horaires-boutique/releases).
2. Dans l'administration, allez dans **Extensions > Ajouter > Téléverser une extension**.
3. Choisissez le fichier zip, puis cliquez sur **Installer maintenant** et **Activer**.

### Manuellement

```bash
cd wp-content/plugins
git clone https://github.com/votre-compte/horaires-boutique.git
```

Activez ensuite l'extension dans **Extensions > Extensions installées**.

## Configuration

Rendez-vous dans **Réglages > Horaires Boutique**.

1. **Horaires** : pour chaque jour, cochez « Fermé » ou ajoutez une ou plusieurs plages horaires.
2. **Fermetures exceptionnelles** : ajoutez des dates (ou des périodes) de fermeture, avec un message facultatif comme « Fermé pour congés jusqu'au 15 août ».
3. **Affichage** :
   - activer ou non l'affichage automatique sur la page d'accueil ;
   - position : avant ou après le contenu ;
   - format : tableau, liste ou compact ;
   - afficher ou masquer l'indicateur d'ouverture.

> Le calcul « ouvert / fermé » utilise le fuseau horaire défini dans **Réglages > Général**. Vérifiez qu'il correspond bien à celui de votre boutique.

## Utilisation

### Page d'accueil

Une fois l'affichage automatique activé, les horaires apparaissent sur la page d'accueil, que ce soit une page statique ou la liste des articles. Aucune autre manipulation n'est nécessaire.

### Shortcode

Pour afficher les horaires dans une page, un article ou un widget texte :

```
[horaires_boutique]
```

Attributs disponibles :

| Attribut  | Valeurs                          | Par défaut     |
|-----------|----------------------------------|----------------|
| `format`  | `tableau`, `liste`, `compact`    | `tableau`      |
| `statut`  | `oui`, `non`                     | `oui`          |
| `titre`   | texte libre                      | `Nos horaires` |

Exemple :

```
[horaires_boutique format="compact" statut="non" titre="Quand passer nous voir ?"]
```

### Bloc Gutenberg

Dans l'éditeur, ajoutez le bloc **Horaires Boutique**. Les options d'affichage se règlent dans le panneau latéral.

### Widget

Dans **Apparence > Widgets**, ajoutez le widget **Horaires Boutique** à la zone de votre choix.

### Dans un thème

```php
<?php
if ( function_exists( 'horaires_boutique_afficher' ) ) {
    horaires_boutique_afficher( array( 'format' => 'liste' ) );
}
?>
```

## Personnalisation

### CSS

Le plugin charge une feuille de style minimale. Les principales classes :

| Classe                         | Élément                           |
|--------------------------------|-----------------------------------|
| `.hb-horaires`                 | Conteneur principal               |
| `.hb-statut--ouvert`           | Indicateur quand la boutique est ouverte |
| `.hb-statut--ferme`            | Indicateur quand elle est fermée  |
| `.hb-jour--aujourdhui`         | Ligne du jour en cours            |
| `.hb-fermeture-exceptionnelle` | Message de fermeture exceptionnelle |

Pour désactiver la feuille de style par défaut :

```php
add_filter( 'horaires_boutique_charger_css', '__return_false' );
```

### Filtres et actions

| Hook                                | Type   | Description                                          |
|-------------------------------------|--------|------------------------------------------------------|
| `horaires_boutique_horaires`        | filtre | Modifie le tableau des horaires avant l'affichage   |
| `horaires_boutique_est_ouvert`      | filtre | Modifie le résultat du calcul ouvert / fermé        |
| `horaires_boutique_html`            | filtre | Modifie le HTML final                                |
| `horaires_boutique_format_heure`    | filtre | Change le format des heures (par défaut `G \h i`)   |
| `horaires_boutique_avant_affichage` | action | S'exécute avant le rendu                             |
| `horaires_boutique_apres_affichage` | action | S'exécute après le rendu                             |

Exemple : afficher les heures au format `09:00`.

```php
add_filter( 'horaires_boutique_format_heure', function () {
    return 'H:i';
} );
```

## Traduction

Le domaine de traduction est `horaires-boutique`. Le fichier modèle se trouve dans `languages/horaires-boutique.pot`. Vous pouvez le traduire avec [Poedit](https://poedit.net/) ou passer par [translate.wordpress.org](https://translate.wordpress.org/).

## FAQ

**Les horaires ne s'affichent pas sur ma page d'accueil.**
Vérifiez que l'affichage automatique est activé dans les réglages. Certains thèmes n'appellent pas `the_content()` sur la page d'accueil : dans ce cas, utilisez le shortcode, le bloc ou la fonction PHP.

**L'indicateur dit « Fermé » alors que la boutique est ouverte.**
Le fuseau horaire de WordPress est probablement mal réglé. Choisissez une ville (par exemple « Paris ») plutôt qu'un décalage UTC, pour que le changement d'heure soit pris en compte.

**Le statut ne se met pas à jour avec mon extension de cache.**
L'indicateur est rafraîchi en JavaScript côté navigateur, il reste donc juste même si la page est en cache. Si vous avez désactivé JavaScript dans les réglages du plugin, excluez la page d'accueil du cache.

**Puis-je gérer plusieurs boutiques ?**
Pas encore. C'est prévu, et les contributions sont les bienvenues.

## Contribuer

Les contributions sont bienvenues : signalement de bugs, traductions, code.

1. Forkez le dépôt.
2. Créez une branche : `git checkout -b ma-fonctionnalite`.
3. Installez les dépendances de développement : `composer install && npm install`.
4. Vérifiez le code avant de proposer vos modifications :
   ```bash
   composer run lint    # WordPress Coding Standards
   composer run test    # PHPUnit
   npm run build        # compilation du bloc
   ```
5. Ouvrez une pull request en décrivant votre modification.

Pour un bug, ouvrez une [issue](https://github.com/votre-compte/horaires-boutique/issues) en précisant vos versions de WordPress et de PHP ainsi que le thème utilisé.

## Journal des modifications

Voir [CHANGELOG.md](CHANGELOG.md).

## Licence

Ce plugin est distribué sous licence [GPL v2 ou ultérieure](https://www.gnu.org/licenses/gpl-2.0.html), comme WordPress.
