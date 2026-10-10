# Démarrage rapide

Ce guide vous permet d'afficher votre premier graphique interactif avec **Lumio Charts** en moins de cinq minutes. Vous y verrez l'installation, la création d'un graphique, sa personnalisation et la mise à jour des données en temps réel.

## Prérequis

- Un navigateur récent : Chrome, Firefox, Safari ou Edge, dans leurs deux dernières versions majeures.
- Node.js 18 ou une version ultérieure, si vous passez par un gestionnaire de paquets.
- Des notions de base en HTML et en JavaScript.

## Installation

### Avec un gestionnaire de paquets

```bash
npm install lumio-charts
```

```bash
# ou
yarn add lumio-charts
# ou
pnpm add lumio-charts
```

Importez ensuite la bibliothèque dans votre code :

```js
import { Chart } from 'lumio-charts';
import 'lumio-charts/dist/lumio.css';
```

### Via un CDN

Pour un prototype ou une page statique, ajoutez simplement ces balises dans votre HTML :

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lumio-charts@3/dist/lumio.css">
<script src="https://cdn.jsdelivr.net/npm/lumio-charts@3/dist/lumio.umd.js"></script>
```

La bibliothèque est alors disponible globalement sous le nom `Lumio`.

## Votre premier graphique

### 1. Préparez un conteneur

Le graphique occupe la taille de son élément parent. Pensez à lui donner une hauteur.

```html
<div id="ventes" style="width: 100%; height: 400px;"></div>
```

### 2. Créez le graphique

```js
import { Chart } from 'lumio-charts';

const chart = new Chart('#ventes', {
  type: 'line',
  data: {
    labels: ['Janv.', 'Févr.', 'Mars', 'Avr.', 'Mai', 'Juin'],
    series: [
      {
        name: 'Ventes 2026',
        values: [120, 150, 170, 140, 210, 260],
      },
    ],
  },
});
```

Ouvrez la page dans votre navigateur : une courbe s'affiche. Survolez un point pour voir l'infobulle, c'est le comportement par défaut.

> **Astuce** : avec la version CDN, remplacez `new Chart(...)` par `new Lumio.Chart(...)`.

## Types de graphiques disponibles

Il suffit de modifier la propriété `type` pour changer de représentation :

| Type | Valeur de `type` | Usage typique |
|------|------------------|---------------|
| Courbe | `'line'` | Évolution dans le temps |
| Barres | `'bar'` | Comparaison entre catégories |
| Aires | `'area'` | Volumes cumulés |
| Secteurs | `'pie'` | Répartition d'un total |
| Nuage de points | `'scatter'` | Corrélation entre deux variables |

## Personnaliser le graphique

Toutes les options se passent dans le même objet de configuration :

```js
const chart = new Chart('#ventes', {
  type: 'bar',
  data: {
    labels: ['Janv.', 'Févr.', 'Mars', 'Avr.'],
    series: [
      { name: '2025', values: [90, 110, 130, 120], color: '#94a3b8' },
      { name: '2026', values: [120, 150, 170, 140], color: '#2563eb' },
    ],
  },
  options: {
    title: 'Ventes mensuelles (k€)',
    locale: 'fr-FR',
    legend: { position: 'bottom' },
    axes: {
      y: {
        min: 0,
        format: (valeur) => `${valeur} k€`,
      },
    },
  },
});
```

L'option `locale: 'fr-FR'` applique le format français aux nombres et aux dates (séparateur décimal, espaces entre les milliers, noms des mois).

## Ajouter de l'interactivité

### Zoom et déplacement

```js
options: {
  zoom: {
    enabled: true,
    mode: 'x', // 'x', 'y' ou 'xy'
  },
}
```

Faites défiler la molette pour zoomer et cliquez-glissez pour vous déplacer. Un double-clic rétablit la vue initiale.

### Infobulles personnalisées

```js
options: {
  tooltip: {
    render: (point) => `
      <strong>${point.label}</strong><br>
      ${point.series} : ${point.value.toLocaleString('fr-FR')} k€
    `,
  },
}
```

### Réagir aux événements

```js
chart.on('click', (point) => {
  console.log(`Vous avez cliqué sur ${point.label} : ${point.value}`);
});

chart.on('legendToggle', ({ series, visible }) => {
  console.log(`${series} est maintenant ${visible ? 'visible' : 'masquée'}`);
});
```

## Mettre à jour les données

Le graphique se redessine avec une animation à chaque modification des données.

```js
// Ajouter un point
chart.append({ label: 'Juil.', values: [280] });

// Remplacer toutes les données
chart.setData({
  labels: ['T1', 'T2', 'T3', 'T4'],
  series: [{ name: 'Ventes', values: [440, 610, 580, 720] }],
});

// Modifier une option
chart.setOptions({ title: 'Ventes trimestrielles' });
```

Exemple d'un flux en temps réel :

```js
setInterval(async () => {
  const reponse = await fetch('/api/ventes/derniere');
  const { label, valeur } = await reponse.json();
  chart.append({ label, values: [valeur] }, { maxPoints: 30 });
}, 5000);
```

L'option `maxPoints` retire les points les plus anciens au-delà de la limite fixée.

## Libérer les ressources

Si vous retirez le graphique de la page, par exemple dans une application monopage, détruisez-le pour libérer les écouteurs d'événements et la mémoire :

```js
chart.destroy();
```

## Utilisation avec un framework

Lumio Charts propose des composants officiels pour les principaux frameworks :

```bash
npm install @lumio-charts/react   # React
npm install @lumio-charts/vue     # Vue 3
npm install @lumio-charts/svelte  # Svelte
```

Exemple avec React :

```jsx
import { LineChart } from '@lumio-charts/react';

export function Ventes({ donnees }) {
  return (
    <LineChart
      data={donnees}
      options={{ locale: 'fr-FR', zoom: { enabled: true } }}
      onClick={(point) => console.log(point)}
      style={{ height: 400 }}
    />
  );
}
```

Le composant met le graphique à jour lorsque `data` change, puis le détruit au démontage.

## Résolution des problèmes courants

**Le graphique ne s'affiche pas.**
Vérifiez que le conteneur a une hauteur non nulle et que le sélecteur (`#ventes`) correspond bien à un élément présent dans le DOM au moment de l'appel.

**Les styles sont absents.**
Vérifiez que vous avez importé `lumio.css`.

**Erreur `Chart is not defined` avec le CDN.**
Utilisez `Lumio.Chart` et assurez-vous que le script est chargé avant votre code.

## Pour aller plus loin

- [Guide des options](./options.md) : référence complète de la configuration
- [Thèmes et styles](./themes.md) : mode sombre et thèmes personnalisés
- [Accessibilité](./accessibilite.md) : navigation au clavier et lecteurs d'écran
- [Performances](./performances.md) : afficher plusieurs centaines de milliers de points
- [Exemples](https://lumio-charts.dev/exemples) : galerie de démonstrations interactives
