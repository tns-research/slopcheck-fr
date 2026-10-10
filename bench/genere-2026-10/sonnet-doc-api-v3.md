# Démarrage rapide

Ce guide vous mène de l'installation à votre premier graphique interactif en quelques minutes.

## Prérequis

- Node.js 18 ou plus récent (pour l'installation via npm)
- Un navigateur moderne (Chrome, Firefox, Safari, Edge)

## Installation

### Via npm

```bash
npm install chartflow
```

### Via un CDN

```html
<script src="https://cdn.jsdelivr.net/npm/chartflow/dist/chartflow.min.js"></script>
```

Avec le CDN, la bibliothèque est exposée dans l'objet global `ChartFlow`.

## Votre premier graphique

### 1. Préparer le conteneur

```html
<div id="graphique" style="width: 600px; height: 400px;"></div>
```

Le conteneur doit avoir une largeur et une hauteur définies. Sans dimensions, le graphique n'est pas visible.

### 2. Créer le graphique

```js
import { Chart } from 'chartflow';

const graphique = new Chart('#graphique', {
  type: 'line',
  data: {
    labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
    datasets: [
      {
        label: 'Visiteurs',
        values: [120, 190, 300, 250, 420, 380],
      },
    ],
  },
  options: {
    title: 'Visiteurs par mois',
    tooltip: true,
  },
});
```

Le graphique s'affiche et réagit immédiatement : survolez un point pour voir son infobulle.

## Types de graphiques

Changez la propriété `type` pour modifier la représentation sans toucher aux données.

| Type | Usage |
|------|-------|
| `line` | Évolution dans le temps |
| `bar` | Comparaison entre catégories |
| `pie` | Répartition d'un total |
| `scatter` | Corrélation entre deux variables |
| `area` | Volumes cumulés dans le temps |

## Ajouter de l'interactivité

Activez le zoom, le déplacement et la légende cliquable depuis `options` :

```js
const graphique = new Chart('#graphique', {
  type: 'bar',
  data: { /* ... */ },
  options: {
    zoom: true,
    pan: true,
    legend: { clickable: true },
  },
});
```

Pour réagir aux actions de l'utilisateur, écoutez les événements :

```js
graphique.on('click', (point) => {
  console.log(`${point.label} : ${point.value}`);
});
```

## Mettre à jour les données

Le graphique se redessine avec une transition fluide quand vous appelez `update` :

```js
graphique.update({
  labels: ['Juil', 'Août', 'Sept'],
  datasets: [{ label: 'Visiteurs', values: [410, 360, 450] }],
});
```

## Adapter le graphique à son conteneur

Par défaut, le graphique suit les changements de taille de son conteneur. Pour désactiver ce comportement :

```js
const graphique = new Chart('#graphique', {
  // ...
  options: { responsive: false },
});
```

## Libérer les ressources

Quand le graphique n'est plus utile (changement de page, démontage d'un composant), détruisez-le pour retirer ses écouteurs d'événements :

```js
graphique.destroy();
```

## Utilisation avec un framework

### React

```jsx
import { useEffect, useRef } from 'react';
import { Chart } from 'chartflow';

export function Graphique({ data }) {
  const ref = useRef(null);

  useEffect(() => {
    const graphique = new Chart(ref.current, { type: 'line', data });
    return () => graphique.destroy();
  }, [data]);

  return <div ref={ref} style={{ width: '100%', height: 400 }} />;
}
```

### Vue

```vue
<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import { Chart } from 'chartflow';

const conteneur = ref(null);
let graphique;

onMounted(() => {
  graphique = new Chart(conteneur.value, { type: 'line', data: { /* ... */ } });
});

onBeforeUnmount(() => graphique.destroy());
</script>

<template>
  <div ref="conteneur" style="width: 100%; height: 400px"></div>
</template>
```

## Problèmes courants

**Le graphique n'apparaît pas.**
Vérifiez que le conteneur existe dans le DOM au moment de l'appel et qu'il a une hauteur non nulle.

**Les infobulles ne s'affichent pas.**
Assurez-vous que `tooltip` vaut `true` et qu'aucun élément avec un `z-index` plus élevé ne recouvre le graphique.

**Le graphique reste figé après un `update`.**
Passez bien un nouvel objet de données à `update`. Modifier le tableau d'origine sur place ne déclenche pas le rendu.

## Étapes suivantes

- [Référence des options](./options.md) : toutes les propriétés de configuration
- [Thèmes et styles](./themes.md) : couleurs, polices et mode sombre
- [Événements](./events.md) : liste complète des interactions disponibles
- [Exemples](./exemples.md) : des graphiques prêts à copier
