# Démarrage rapide

Créez votre premier graphique interactif en quelques minutes avec **NovaChart**.

## Installation

Installez la bibliothèque avec npm :

```bash
npm install novachart
```

Ou chargez-la directement depuis un CDN :

```html
<script src="https://cdn.example.com/novachart.min.js"></script>
```

## Créer un graphique

Ajoutez un conteneur dans votre page :

```html
<div id="chart"></div>
```

Importez ensuite la bibliothèque et créez le graphique :

```js
import { Chart } from "novachart";

const chart = new Chart("#chart", {
  type: "line",
  data: {
    labels: ["Janvier", "Février", "Mars", "Avril"],
    datasets: [
      {
        label: "Ventes",
        data: [12, 19, 8, 24],
        color: "#6366f1"
      }
    ]
  },
  options: {
    responsive: true,
    interactive: true,
    title: "Ventes mensuelles"
  }
});
```

Le graphique s’adapte automatiquement à la taille de son conteneur. Le survol, les infobulles et la navigation au clavier sont activés par défaut.

## Définir la taille

Le conteneur doit posséder une hauteur explicite :

```css
#chart {
  width: 100%;
  height: 400px;
}
```

## Mettre à jour les données

Utilisez `setData()` pour modifier le graphique sans le recréer :

```js
chart.setData({
  labels: ["Mai", "Juin", "Juillet"],
  datasets: [
    {
      label: "Ventes",
      data: [28, 21, 35],
      color: "#6366f1"
    }
  ]
});
```

Les transitions sont animées automatiquement. Pour les désactiver :

```js
chart.setData(newData, { animate: false });
```

## Réagir aux interactions

Abonnez-vous aux événements émis par le graphique :

```js
chart.on("point:click", ({ label, value, dataset }) => {
  console.log(`${dataset} — ${label} : ${value}`);
});
```

Événements courants :

| Événement | Déclenchement |
|---|---|
| `point:click` | Clic sur un point ou une barre |
| `point:hover` | Survol d’une valeur |
| `legend:toggle` | Affichage ou masquage d’une série |
| `zoom` | Modification de la zone visible |

## Détruire le graphique

Lorsque le graphique n’est plus utilisé, libérez ses ressources :

```js
chart.destroy();
```

Cette opération supprime les écouteurs d’événements, les observateurs de redimensionnement et les éléments graphiques générés.

## Exemple complet

```html
<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Mon premier graphique</title>

    <style>
      #chart {
        width: 100%;
        height: 400px;
      }
    </style>
  </head>

  <body>
    <div id="chart"></div>

    <script type="module">
      import { Chart } from "https://cdn.example.com/novachart.esm.js";

      const chart = new Chart("#chart", {
        type: "bar",
        data: {
          labels: ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
          datasets: [
            {
              label: "Visites",
              data: [120, 180, 150, 230, 260],
              color: "#14b8a6"
            }
          ]
        },
        options: {
          responsive: true,
          interactive: true,
          title: "Visites de la semaine"
        }
      });

      chart.on("point:click", ({ label, value }) => {
        alert(`${label} : ${value} visites`);
      });
    </script>
  </body>
</html>
```

## Étapes suivantes

- Découvrez les graphiques disponibles : courbes, barres, aires, secteurs et nuages de points.
- Personnalisez les couleurs, axes, légendes, infobulles et animations.
- Activez le zoom, la sélection et le streaming de données.
- Consultez la référence de l’API pour connaître toutes les options disponibles.