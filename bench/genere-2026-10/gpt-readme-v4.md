# Horaires Boutique

Plugin WordPress open source permettant d’afficher les horaires d’ouverture d’une boutique sur la page d’accueil.

## Fonctionnalités

- Configuration des horaires pour chaque jour de la semaine
- Gestion des jours fermés
- Affichage automatique sur la page d’accueil
- Indication « Ouvert » ou « Fermé » en temps réel
- Prise en charge des horaires fractionnés
- Shortcode utilisable partout
- Mise en page responsive
- Compatible avec la plupart des thèmes WordPress
- Traductions prêtes à l’emploi

## Prérequis

- WordPress 6.0 ou supérieur
- PHP 8.0 ou supérieur

## Installation

1. Téléchargez le plugin.
2. Copiez le dossier `horaires-boutique` dans `/wp-content/plugins/`.
3. Activez **Horaires Boutique** depuis le menu **Extensions** de WordPress.
4. Accédez à **Réglages → Horaires Boutique**.
5. Configurez les horaires, puis enregistrez les modifications.

## Utilisation

### Affichage automatique

Activez l’option **Afficher sur la page d’accueil** dans les réglages du plugin.

Vous pouvez choisir d’afficher les horaires :

- avant le contenu principal ;
- après le contenu principal ;
- dans une zone gérée par votre thème.

### Shortcode

Ajoutez le shortcode suivant dans une page, un article ou un widget :

```text
[horaires_boutique]
```

Pour afficher uniquement le statut actuel :

```text
[horaires_boutique affichage="statut"]
```

Pour afficher uniquement les horaires de la journée :

```text
[horaires_boutique affichage="aujourdhui"]
```

## Exemple

```text
Horaires d’ouverture

Lundi       09:00–12:30 / 14:00–18:30
Mardi       09:00–12:30 / 14:00–18:30
Mercredi    09:00–12:30 / 14:00–18:30
Jeudi       09:00–12:30 / 14:00–18:30
Vendredi    09:00–12:30 / 14:00–18:30
Samedi      10:00–18:00
Dimanche    Fermé

Ouvert actuellement
```

## Personnalisation

Le composant utilise les classes CSS suivantes :

```css
.horaires-boutique {}
.horaires-boutique__titre {}
.horaires-boutique__liste {}
.horaires-boutique__jour {}
.horaires-boutique__jour--actuel {}
.horaires-boutique__statut {}
.horaires-boutique__statut--ouvert {}
.horaires-boutique__statut--ferme {}
```

Exemple de personnalisation :

```css
.horaires-boutique {
  padding: 1.5rem;
  border-radius: 0.5rem;
  background: #f5f5f5;
}

.horaires-boutique__jour--actuel {
  font-weight: 700;
}

.horaires-boutique__statut--ouvert {
  color: #16803c;
}

.horaires-boutique__statut--ferme {
  color: #b42318;
}
```

## Fuseau horaire

Le plugin utilise le fuseau horaire configuré dans **Réglages → Général → Fuseau horaire**. Vérifiez ce réglage afin que le statut d’ouverture soit exact.

## Développement

Clonez le dépôt dans le dossier des extensions WordPress :

```bash
git clone https://github.com/votre-compte/horaires-boutique.git \
  wp-content/plugins/horaires-boutique
```

Créez une branche pour votre modification :

```bash
git switch -c amelioration/ma-fonctionnalite
```

Avant de proposer une contribution, vérifiez que :

- le code respecte les standards de développement WordPress ;
- les données saisies sont validées et échappées ;
- les textes affichés sont traduisibles ;
- la modification reste compatible avec les versions prises en charge.

## Signaler un problème

Ouvrez une issue en précisant :

- la version de WordPress ;
- la version de PHP ;
- le thème utilisé ;
- les étapes permettant de reproduire le problème ;
- les éventuels messages d’erreur.

N’incluez jamais de mot de passe, de clé API ou de donnée personnelle.

## Contribution

Les contributions sont les bienvenues. Vous pouvez proposer une correction, une amélioration de l’accessibilité, une traduction ou une nouvelle fonctionnalité via une pull request.

## Licence

Ce projet est distribué sous licence [GPL-2.0-or-later](https://www.gnu.org/licenses/gpl-2.0.html).

Vous êtes libre de l’utiliser, de le modifier et de le redistribuer conformément aux conditions de cette licence.