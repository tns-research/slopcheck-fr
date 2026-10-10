# Démarrage rapide

Ce guide vous permet d'effectuer votre première réservation de salle en moins de dix minutes. Vous allez obtenir une clé d'API, lister les salles disponibles, créer une réservation, puis l'annuler.

## Prérequis

- Un compte administrateur ou développeur sur votre espace de travail.
- `curl` ou tout autre client HTTP.
- Des notions de base sur les API REST et le format JSON.

## 1. Obtenir une clé d'API

1. Connectez-vous à la console d'administration.
2. Ouvrez **Paramètres › Développeurs › Clés d'API**.
3. Cliquez sur **Générer une clé**, donnez-lui un nom (par exemple `test-local`), puis copiez-la.

> **Important :** la clé ne s'affiche qu'une seule fois. Conservez-la dans un gestionnaire de secrets et ne la versionnez jamais dans votre dépôt.

Pour la suite du guide, enregistrez-la dans une variable d'environnement :

```bash
export API_KEY="sk_test_votre_cle"
export API_URL="https://api.exemple.com/v1"
```

## 2. Vérifier l'authentification

Toutes les requêtes doivent inclure l'en-tête `Authorization` au format `Bearer`.

```bash
curl "$API_URL/me" \
  -H "Authorization: Bearer $API_KEY"
```

Réponse attendue :

```json
{
  "id": "usr_8f2k1",
  "email": "vous@exemple.com",
  "organization": "org_42ab"
}
```

Si vous obtenez une erreur `401 Unauthorized`, vérifiez que la clé est complète et qu'elle n'a pas été révoquée.

## 3. Lister les salles disponibles

Recherchez les salles libres sur un créneau donné. Les dates sont exprimées au format ISO 8601, avec le fuseau horaire.

```bash
curl -G "$API_URL/rooms" \
  -H "Authorization: Bearer $API_KEY" \
  --data-urlencode "available_from=2026-10-15T09:00:00+02:00" \
  --data-urlencode "available_to=2026-10-15T10:00:00+02:00" \
  --data-urlencode "min_capacity=6"
```

Réponse :

```json
{
  "data": [
    {
      "id": "room_paris_3a",
      "name": "Salle Montmartre",
      "site": "Paris – 3e étage",
      "capacity": 8,
      "equipment": ["ecran", "visioconference", "tableau_blanc"]
    }
  ],
  "has_more": false
}
```

Notez l'`id` de la salle : vous en aurez besoin à l'étape suivante.

## 4. Créer une réservation

```bash
curl -X POST "$API_URL/bookings" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 5d1c7e0a-reunion-equipe" \
  -d '{
    "room_id": "room_paris_3a",
    "title": "Point hebdomadaire",
    "start": "2026-10-15T09:00:00+02:00",
    "end": "2026-10-15T10:00:00+02:00",
    "attendees": ["alice@exemple.com", "karim@exemple.com"]
  }'
```

Réponse `201 Created` :

```json
{
  "id": "bkg_7Hq92",
  "status": "confirmed",
  "room_id": "room_paris_3a",
  "title": "Point hebdomadaire",
  "start": "2026-10-15T09:00:00+02:00",
  "end": "2026-10-15T10:00:00+02:00",
  "created_at": "2026-10-09T14:21:07Z"
}
```

> **Astuce :** l'en-tête `Idempotency-Key` évite les doublons si vous renvoyez la même requête après une coupure réseau. Utilisez une valeur unique par réservation.

Si le créneau est déjà pris entre-temps, l'API renvoie `409 Conflict` :

```json
{
  "error": {
    "code": "slot_unavailable",
    "message": "La salle est déjà réservée sur ce créneau."
  }
}
```

## 5. Consulter la réservation

```bash
curl "$API_URL/bookings/bkg_7Hq92" \
  -H "Authorization: Bearer $API_KEY"
```

## 6. Annuler la réservation

```bash
curl -X DELETE "$API_URL/bookings/bkg_7Hq92" \
  -H "Authorization: Bearer $API_KEY"
```

L'API renvoie `204 No Content`. Les participants reçoivent automatiquement une notification d'annulation.

## Codes d'erreur courants

| Code HTTP | Signification | Que faire ? |
|-----------|---------------|-------------|
| `400` | Requête invalide | Vérifiez le format des dates et les champs obligatoires. |
| `401` | Clé absente ou invalide | Contrôlez l'en-tête `Authorization`. |
| `403` | Droits insuffisants | Demandez l'accès à la salle ou au site concerné. |
| `404` | Ressource introuvable | Vérifiez l'identifiant de la salle ou de la réservation. |
| `409` | Créneau indisponible | Choisissez un autre créneau ou une autre salle. |
| `429` | Trop de requêtes | Attendez la durée indiquée dans l'en-tête `Retry-After`. |

## Limites de débit

Par défaut, chaque clé est limitée à **100 requêtes par minute**. Les en-têtes `X-RateLimit-Remaining` et `X-RateLimit-Reset` indiquent votre consommation en temps réel.

## Étapes suivantes

- **Webhooks** : recevez un événement à chaque création, modification ou annulation de réservation.
- **Réservations récurrentes** : planifiez des réunions hebdomadaires avec le champ `recurrence`.
- **SDK officiels** : bibliothèques disponibles pour JavaScript, Python et Java.
- **Référence de l'API** : consultez la liste complète des points de terminaison et de leurs paramètres.

Une question ? Écrivez-nous à support@exemple.com.
