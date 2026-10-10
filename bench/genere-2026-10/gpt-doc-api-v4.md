# Démarrage rapide

Cette API permet de consulter les salles disponibles et de créer une réservation en quelques requêtes HTTP.

## Prérequis

Vous aurez besoin de votre clé d’API, disponible dans le tableau de bord.

```bash
export ROOM_API_KEY="votre_cle_api"
```

L’URL de base de l’API est :

```text
https://api.exemple.com/v1
```

## 1. Vérifier les salles disponibles

Recherchez les salles disponibles pour un créneau donné :

```bash
curl --request GET \
  --url "https://api.exemple.com/v1/rooms/availability?starts_at=2026-10-12T09:00:00Z&ends_at=2026-10-12T10:00:00Z&capacity=6" \
  --header "Authorization: Bearer $ROOM_API_KEY" \
  --header "Accept: application/json"
```

Exemple de réponse :

```json
{
  "data": [
    {
      "id": "room_atlas",
      "name": "Atlas",
      "capacity": 8,
      "equipment": [
        "screen",
        "videoconference",
        "whiteboard"
      ]
    }
  ]
}
```

Toutes les dates doivent être envoyées au format ISO 8601 avec un fuseau horaire explicite.

## 2. Créer une réservation

Utilisez l’identifiant de la salle retourné par la requête précédente :

```bash
curl --request POST \
  --url "https://api.exemple.com/v1/bookings" \
  --header "Authorization: Bearer $ROOM_API_KEY" \
  --header "Content-Type: application/json" \
  --header "Idempotency-Key: reunion-equipe-2026-10-12-09h" \
  --data '{
    "room_id": "room_atlas",
    "starts_at": "2026-10-12T09:00:00Z",
    "ends_at": "2026-10-12T10:00:00Z",
    "title": "Réunion d’équipe",
    "organizer": {
      "name": "Camille Martin",
      "email": "camille@example.com"
    },
    "attendees": 6
  }'
```

L’en-tête `Idempotency-Key` évite de créer plusieurs réservations si la requête est renvoyée accidentellement.

Exemple de réponse avec le statut `201 Created` :

```json
{
  "id": "bkg_01J9Y8X7W6",
  "status": "confirmed",
  "room": {
    "id": "room_atlas",
    "name": "Atlas"
  },
  "starts_at": "2026-10-12T09:00:00Z",
  "ends_at": "2026-10-12T10:00:00Z",
  "title": "Réunion d’équipe",
  "organizer": {
    "name": "Camille Martin",
    "email": "camille@example.com"
  },
  "attendees": 6,
  "created_at": "2026-10-09T14:32:10Z"
}
```

## 3. Consulter la réservation

```bash
curl --request GET \
  --url "https://api.exemple.com/v1/bookings/bkg_01J9Y8X7W6" \
  --header "Authorization: Bearer $ROOM_API_KEY" \
  --header "Accept: application/json"
```

## 4. Annuler la réservation

```bash
curl --request DELETE \
  --url "https://api.exemple.com/v1/bookings/bkg_01J9Y8X7W6" \
  --header "Authorization: Bearer $ROOM_API_KEY"
```

Une annulation réussie renvoie le statut `204 No Content`.

## Gestion des erreurs

Les erreurs suivent une structure commune :

```json
{
  "error": {
    "code": "room_unavailable",
    "message": "La salle n’est plus disponible pour ce créneau.",
    "request_id": "req_01J9Y9A2BC"
  }
}
```

| Statut | Signification |
|---:|---|
| `400` | Paramètres invalides |
| `401` | Clé d’API absente ou invalide |
| `404` | Salle ou réservation introuvable |
| `409` | Salle indisponible pour le créneau demandé |
| `422` | Données valides mais réservation impossible |
| `429` | Limite de requêtes dépassée |
| `500` | Erreur interne du service |

Conservez la valeur `request_id` lorsque vous contactez l’assistance : elle permet d’identifier rapidement la requête concernée.