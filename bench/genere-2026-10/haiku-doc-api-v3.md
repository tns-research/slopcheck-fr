# Démarrage rapide

Ce guide vous permet d'afficher votre premier graphique interactif en quelques minutes.

## Prérequis

- Node.js 18 ou supérieur
- Un navigateur moderne (Chrome, Firefox, Safari, Edge)

## Installation

Installez la bibliothèque avec votre gestionnaire de paquets :

```bash
npm install lumiplot
```

Vous pouvez aussi l'charger directement depuis un CDN :

```html
<script src="https://cdn.example.com/lumiplot/latest/lumiplot.min.js"></script>
```

## Votre premier graphique

1. Ajoutez un conteneur dans votre page HTML. Le graphique prend la taille de ce conteneur.

```html
<div id="mon-graphique" style="width: 600px; height: 400px;"></div>
```

2. Importez la bibliothèque et créez le graphique avec vos données :

```javascript
import { Lumiplot } from 'lumiplot';

const graphique = new Lumiplot('#mon-graphique', {
  type: 'ligne',
  titre: 'Ventes mensuelles',
  donnees: {
    labels: ['Janv.', 'Févr.', 'Mars', 'Avril', 'Mai', 'Juin'],
    series: [
      {
        nom: '2025',
        valeurs: [120, 145, 132, 170, 158, 190]
      },
      {
        nom: '2026',
        valeurs: [135, 160, 150, 183, 175, 210]
      }
    ]
  }
});
```

Le graphique s'affiche dès l'appel au constructeur.

## Interactions incluses

Sans configuration supplémentaire, le graphique répond à l'utilisateur :

- **Survol** : une infobulle affiche la valeur du point ou de la barre sous le curseur.
- **Légende** : un clic sur un nom de série masque ou affiche cette série.
- **Zoom** : faites glisser la souris sur une zone pour zoomer, puis double-cliquez pour revenir à la vue initiale.
- **Tactile** : pincez pour zoomer et faites glisser pour vous déplacer sur mobile et tablette.

## Types de graphiques

| Type | Valeur de `type` | Usage typique |
|---|---|---|
| Ligne | `'ligne'` | Évolutions dans le temps |
| Barres | `'barres'` | Comparaison entre catégories |
| Aires | `'aires'` | Volumes cumulés |
| Nuage de points | `'points'` | Corrélations entre deux variables |
| Secteurs | `'secteurs'` | Répartition d'un total |

Pour changer de type, modifiez simplement la valeur de `type` :

```javascript
graphique.configurer({ type: 'barres' });
```

## Écouter les événements

Réagissez aux actions de l'utilisateur avec `on()` :

```javascript
graphique.on('clic', (evenement) => {
  console.log('Point cliqué :', evenement.label, evenement.valeur);
});

graphique.on('selection', (plage) => {
  console.log('Plage sélectionnée :', plage.debut, '→', plage.fin);
});
```

## Mettre à jour les données

Pour rafraîchir le graphique, appelez `mettreAJour()`. L'animation de transition est appliquée automatiquement :

```javascript
graphique.mettreAJour({
  series: [
    { nom: '2026', valeurs: [140, 165, 158, 190, 181, 220] }
  ]
});
```

## Libérer les ressources

Lorsque le graphique n'est plus nécessaire, par exemple avant de retirer son conteneur du DOM, détruisez-le :

```javascript
graphique.detruire();
```

## Étapes suivantes

- **Options de configuration** : axes, couleurs, thèmes et animations
- **Réfèrence de l'API** : méthodes, événements et types de données
- **Exemples** : tableaux de bord, graphiques temps réel et intégrations avec React, Vue et Svelte
