# Démarrage rapide

Cette page vous guide de la création d'une clé d'API jusqu'à votre première réservation de salle de réunion, en quelques minutes.

## Prérequis

- Un compte avec accès à la console développeur
- `curl`, ou tout client HTTP de votre choix

## 1. Obtenir une clé d'API

1. Ouvrez la console développeur, section **Clés d'API**.
2. Cliquez sur **Créer une clé**.
3. Copiez la clé immédiatement : elle ne sera plus affichée ensuite.

Stockez-la dans une variable d'environnement. Ne la versionnez jamais dans votre dépôt.

```bash
export API_KEY="sk_test_votre_cle"
```

## 2. URL de base et authentification

Toutes les requêtes passent par HTTPS et s'authentifient avec un jeton Bearer.

```
https://api.example.com/v1
```

```bash
curl https://api.example.com/v1/rooms \
  -H "Authorization: Bearer $API_KEY"
```

> Les clés préfixées par `sk_test_` accèdent à l'environnement de test, où aucune réservation réelle n'est créée. Les clés `sk_live_` agissent en production.

## 3. Lister les salles

```bash
curl "https://api.example.com/v1/rooms?capacity_min=6&equipment=visio" \
  -H "Authorization: Bearer $API_KEY"
```

Réponse :

```json
{
  "data": [
    {
      "id": "room_8f3a2c",
      "name": "Salle Lumière",
      "capacity": 8,
      "floor": 2,
      "equipment": ["visio", "ecran", "tableau-blanc"]
    }
  ],
  "has_more": false
}
```

## 4. Vérifier les disponibilités

```bash
curl "https://api.example.com/v1/rooms/room_8f3a2c/availability?start=2026-10-15T09:00:00Z&end=2026-10-15T18:00:00Z" \
  -H "Authorization: Bearer $API_KEY"
```

Réponse :

```json
{
  "room_id": "room_8f3a2c",
  "free_slots": [
    { "start": "2026-10-15T09:00:00Z", "end": "2026-10-15T11:00:00Z" },
    { "start": "2026-10-15T14:00:00Z", "end": "2026-10-15T18:00:00Z" }
  ]
}
```

## 5. Créer une réservation

```bash
curl -X POST https://api.example.com/v1/bookings \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 6f1c9e52-4b7a-4d1e-9a30-2c5e8b7d1f04" \
  -d '{
    "room_id": "room_8f3a2c",
    "title": "Point hebdomadaire équipe produit",
    "start": "2026-10-15T09:30:00Z",
    "end": "2026-10-15T10:30:00Z",
    "attendees": ["alice@example.com", "karim@example.com"]
  }'
```

Réponse (`201 Created`) :

```json
{
  "id": "bk_41d7e0",
  "room_id": "room_8f3a2c",
  "title": "Point hebdomadaire équipe produit",
  "start": "2026-10-15T09:30:00Z",
  "end": "2026-10-15T10:30:00Z",
  "status": "confirmed"
}
```

L'en-tête `Idempotency-Key` est facultatif mais recommandé : si vous rejouez la même requête avec la même clé (après un timeout réseau, par exemple), la réservation n'est créée qu'une seule fois.

## 6. Modifier ou annuler une réservation

```bash
# Déplacer la réunion d'une heure
curl -X PATCH https://api.example.com/v1/bookings/bk_41d7e0 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "start": "2026-10-15T10:30:00Z", "end": "2026-10-15T11:30:00Z" }'

# Annuler
curl -X DELETE https://api.example.com/v1/bookings/bk_41d7e0 \
  -H "Authorization: Bearer $API_KEY"
```

## Exemple en JavaScript

```javascript
const res = await fetch("https://api.example.com/v1/bookings", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    room_id: "room_8f3a2c",
    title: "Point hebdomadaire équipe produit",
    start: "2026-10-15T09:30:00Z",
    end: "2026-10-15T10:30:00Z",
  }),
});

if (!res.ok) {
  const { error } = await res.json();
  throw new Error(`${error.code} : ${error.message}`);
}

const booking = await res.json();
console.log(booking.id);
```

## Gestion des erreurs

Les erreurs renvoient un code HTTP approprié et un corps JSON uniforme :

```json
{
  "error": {
    "code": "slot_unavailable",
    "message": "La salle est déjà réservée sur ce créneau."
  }
}
```

| Code HTTP | `error.code` | Signification |
|---|---|---|
| 400 | `invalid_request` | Paramètre manquant ou mal formé |
| 401 | `unauthorized` | Clé d'API absente ou invalide |
| 404 | `not_found` | Salle ou réservation introuvable |
| 409 | `slot_unavailable` | Le créneau est déjà occupé |
| 429 | `rate_limited` | Trop de requêtes, réessayez plus tard |
| 500 | `internal_error` | Erreur côté serveur |

## Bonnes pratiques

- **Dates** : utilisez toujours le format ISO 8601 en UTC (`2026-10-15T09:30:00Z`).
- **Limite de débit** : 100 requêtes par minute et par clé. En cas de `429`, respectez l'en-tête `Retry-After`.
- **Pagination** : les listes utilisent `limit` (50 maximum) et `starting_after`.
- **Conflits** : vérifiez les disponibilités juste avant de réserver, et gérez le `409` pour les réservations simultanées.

## Prochaines étapes

- [Référence de l'API](#) : tous les endpoints et paramètres
- [Webhooks](#) : recevez une notification à chaque création, modification ou annulation
- [Réservations récurrentes](#) : planifiez des réunions hebdomadaires
- [SDK officiels](#) : bibliothèques JavaScript, Python et PHP

Une question ? Écrivez-nous à `support@example.com`.
