```markdown
# Horaires Boutique

Plugin WordPress open source pour afficher les horaires d'ouverture de votre boutique sur la page d'accueil de votre site.

![Licence GPL v2+](https://img.shields.io/badge/licence-GPL--2.0%2B-blue)
![WordPress 6.0+](https://img.shields.io/badge/WordPress-6.0%2B-21759b)
![PHP 7.4+](https://img.shields.io/badge/PHP-7.4%2B-777bb4)

## Fonctionnalités

- Saisie des horaires jour par jour, avec plusieurs plages par jour (par exemple 9 h à 12 h, puis 14 h à 19 h).
- Gestion des jours de fermeture et des fermetures exceptionnelles (jours fériés, congés, inventaire).
- Badge « Ouvert maintenant » ou « Fermé » calculé selon le fuseau horaire du site.
- Affichage sur la page d'accueil automatique, ou à l'endroit de votre choix via un bloc, un shortcode ou un widget.
- Balisage `schema.org` (`OpeningHoursSpecification`) pour aider le référencement local.
- Compatible avec les thèmes classiques et les thèmes de blocs (FSE).
- Traduit en français, prêt pour la traduction dans d'autres langues.
- Aucun appel à un service externe, aucun cookie, aucune donnée collectée.

## Prérequis

- WordPress 6.0 ou supérieur
- PHP 7.4 ou supérieur

## Installation

### Depuis l'administration WordPress

1. Allez dans **Extensions > Ajouter**.
2. Recherchez « Horaires Boutique ».
3. Cliquez sur **Installer**, puis sur **Activer**.

### Manuellement

1. Téléchargez la dernière version depuis la page [Releases](https://github.com/votre-organisation/horaires-boutique/releases).
2. Décompressez l'archive dans `wp-content/plugins/`.
3. Activez le plugin depuis **Extensions**.

### Depuis les sources

```bash
cd wp-content/plugins
git clone https://github.com/votre-organisation/horaires-boutique.git
cd horaires-boutique
composer install --no-dev
npm install && npm run build
```

## Configuration

1. Ouvrez **Réglages > Horaires Boutique**.
2. Renseignez les horaires pour chaque jour de la semaine.
3. Ajoutez vos fermetures exceptionnelles avec une date et un motif facultatif.
4. Choisissez l'emplacement d'affichage et enregistrez.

## Utilisation

### Affichage automatique sur la page d'accueil

Dans **Réglages > Horaires Boutique**, activez l'option « Afficher sur la page d'accueil » et choisissez la position : avant ou après le contenu.

### Bloc Gutenberg

Dans l'éditeur, ajoutez le bloc **Horaires Boutique**. Les options d'affichage se règlent dans le panneau latéral.

### Shortcode

```
[horaires_boutique]
```

Attributs disponibles :

| Attribut | Valeurs | Défaut | Description |
|---|---|---|---|
| `badge` | `oui`, `non` | `oui` | Affiche le badge « Ouvert » ou « Fermé » |
| `format` | `24h`, `12h` | `24h` | Format de l'heure |
| `jours` | `complet`, `abrege` | `complet` | Noms des jours en entier ou abrégés |
| `aujourdhui` | `oui`, `non` | `oui` | Met en évidence le jour en cours |

Exemple :

```
[horaires_boutique badge="non" jours="abrege"]
```

### Fonction PHP

Pour les développeurs de thèmes :

```php
<?php
if ( function_exists( 'horaires_boutique_afficher' ) ) {
    horaires_boutique_afficher( array( 'badge' => 'oui' ) );
}
```

## Personnalisation

Le plugin génère un balisage simple, facile à styliser :

```html
<div class="horaires-boutique">
  <p class="horaires-boutique__statut horaires-boutique__statut--ouvert">Ouvert maintenant</p>
  <ul class="horaires-boutique__liste">
    <li class="horaires-boutique__jour horaires-boutique__jour--aujourdhui">
      <span class="horaires-boutique__nom">Lundi</span>
      <span class="horaires-boutique__heures">9 h – 12 h, 14 h – 19 h</span>
    </li>
  </ul>
</div>
```

### Filtres

```php
// Modifier le texte du badge.
add_filter( 'horaires_boutique_texte_ouvert', function () {
    return 'Venez nous voir !';
} );

// Modifier les horaires avant l'affichage.
add_filter( 'horaires_boutique_horaires', function ( $horaires ) {
    return $horaires;
} );
```

### Surcharge du modèle

Copiez `templates/horaires.php` dans `votre-theme/horaires-boutique/horaires.php` pour adapter entièrement le rendu.

## Questions fréquentes

**Le badge « Ouvert » affiche une mauvaise heure.**
Vérifiez le fuseau horaire dans **Réglages > Général**. Le plugin s'appuie sur ce réglage.

**Puis-je gérer plusieurs boutiques ?**
Pas dans la version actuelle. Cette fonctionnalité est prévue (voir la feuille de route).

**Le plugin ralentit-il mon site ?**
Non. Les horaires sont lus depuis une seule option en base et le rendu est mis en cache le temps de la requête. Le CSS fait moins de 2 Ko.

**Le plugin est-il conforme au RGPD ?**
Il ne collecte aucune donnée personnelle et ne dépose aucun cookie.

## Feuille de route

- [ ] Gestion de plusieurs établissements
- [ ] Import et export des horaires au format JSON
- [ ] Horaires saisonniers programmés à l'avance
- [ ] Intégration avec WooCommerce (message de délai de préparation)

## Contribuer

Les contributions sont les bienvenues.

1. Forkez le dépôt.
2. Créez une branche : `git checkout -b ma-fonctionnalite`.
3. Installez les dépendances : `composer install && npm install`.
4. Vérifiez le code : `composer lint` et `npm test`.
5. Ouvrez une *pull request* en décrivant le changement.

Pour signaler un bug ou proposer une idée, ouvrez une [issue](https://github.com/votre-organisation/horaires-boutique/issues). Merci d'indiquer vos versions de WordPress et de PHP, ainsi que votre thème.

### Traductions

Les traductions se font sur [translate.wordpress.org](https://translate.wordpress.org/projects/wp-plugins/horaires-boutique/). Le fichier `.pot` se trouve dans `languages/`.

## Sécurité

Pour signaler une faille, n'ouvrez pas d'issue publique. Écrivez à `securite@exemple.org`. Nous répondons sous 72 heures.

## Journal des modifications

Voir [CHANGELOG.md](CHANGELOG.md).

## Licence

Ce projet est distribué sous licence [GPL v2 ou ultérieure](LICENSE), comme WordPress.
```
