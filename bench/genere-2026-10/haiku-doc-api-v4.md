# Démarrage rapide

Ce guide vous permet de réserver une salle de réunion par API en moins de dix minutes.

## Prérequis

- Un compte sur le tableau de bord, avec le rôle **Développeur**
- `curl` ou un client HTTP équivalent
- Un espace de travail (*workspace*) auquel vous êtes rattaché

## 1. Obtenir une clé d'API

1. Ouvrez **Paramètres → Intégrations → Clés d'API**.
2. Cliquez sur **Créer une clé**, puis donnez-lui un nom explicite, par exemple `intranet-prod`.
3. Copiez la clé immédiatement. Elle n'est affichée qu'une seule fois.

Conservez la clé dans une variable d'environnement, jamais dans le code source :

```bash
export RESA_API_KEY="sk_live_votre_cle"
```

## 2. Vérifier la connexion

Appelez l'endpoint d'identité pour confirmer que votre clé fonctionne :

```bash
curl https://api.reservesalles.example/v1/me \
  -H "Authorization: Bearer $RESA_API_KEY"
```

Réponse attendue (`200 OK`) :

```json
{
  "id": "usr_8f3K2a",
  "email": "dev@exemple.fr",
  "workspace": {
    "id": "ws_41Qd9",
    "name": "Siège Lyon"
  }
}
```

## 3. Lister les salles disponibles

```bash
curl "https://api.reservesalles.example/v1/rooms?capacity_min=6&floor=2" \
  -H "Authorization: Bearer $RESA_API_KEY"
```

Chaque salle renvoie un identifiant `id` que vous utiliserez pour la réservation :

```json
{
  "data": [
    {
      "id": "room_Lx7Pm",
      "name": "Mont-Blanc",
      "capacity": 8,
      "floor": 2,
      "equipment": ["visioconférence", "tableau_blanc"]
    }
  ],
  "next_cursor": null
}
```

## 4. Vérifier un créneau

Avant de réserver, interrogez la disponibilité. Les dates sont au format ISO 8601 avec fuseau horaire.

```bash
curl "https://api.reservesalles.example/v1/rooms/room_Lx7Pm/availability?start=2026-10-12T09:00:00%2B02:00&end=2026-10-12T10:00:00%2B02:00" \
  -H "Authorization: Bearer $RESA_API_KEY"
```

```json
{
  "room_id": "room_Lx7Pm",
  "available": true,
  "conflicts": []
}
```

## 5. Créer une réservation

```bash
curl -X POST https://api.reservesalles.example/v1/bookings \
  -H "Authorization: Bearer $RESA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 4c0b7e2a-9d1f-4f6e-8a31-2b5c9e7d1a02" \
  -d '{
    "room_id": "room_Lx7Pm",
    "title": "Revue sprint 42",
    "start": "2026-10-12T09:00:00+02:00",
    "end": "2026-10-12T10:00:00+02:00",
    "attendees": ["alice@exemple.fr", "bruno@exemple.fr"]
  }'
```

Réponse (`201 Created`) :

```json
{
  "id": "bkg_R9tYw",
  "status": "confirmed",
  "room_id": "room_Lx7Pm",
  "start": "2026-10-12T09:00:00+02:00",
  "end": "2026-10-12T10:00:00+02:00"
}
```

> **Astuce :** l'en-tête `Idempotency-Key` évite les doubles réservations en cas de nouvelle tentative réseau. Utilisez un UUID v4 unique par intention de réservation, et réutilisez-le lors d'un nouvel essai.

## 6. Annuler une réservation

```bash
curl -X DELETE https://api.reservesalles.example/v1/bookings/bkg_R9tYw \
  -H "Authorization: Bearer $RESA_API_KEY"
```

La réponse est `204 No Content`.

## Exemple complet en Python

```python
import os
import requests

BASE_URL = "https://api.reservesalles.example/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['RESA_API_KEY']}"}

booking = requests.post(
    f"{BASE_URL}/bookings",
    headers={**HEADERS, "Idempotency-Key": "4c0b7e2a-9d1f-4f6e-8a31-2b5c9e7d1a02"},
    json={
        "room_id": "room_Lx7Pm",
        "title": "Revue sprint 42",
        "start": "2026-10-12T09:00:00+02:00",
        "end": "2026-10-12T10:00:00+02:00",
        "attendees": ["alice@exemple.fr"],
    },
    timeout=10,
)
booking.raise_for_status()
print(booking.json()["id"])
```

## Codes d'erreur courants

| Code | Signification | Action |
|------|---------------|--------|
| `401` | Clé absente ou invalide | Vérifiez l'en-tête `Authorization` |
| `403` | Rôle insuffisant pour cette salle | Demandez l'accès à un administrateur |
| `409` | Créneau déjà réservé | Relancez la disponibilité avec un autre horaire |
| `422` | Données invalides (ex. fin avant début) | Corrigez le corps de la requête |
| `429` | Limite de débit atteinte (120 req/min) | Attendez la valeur de l'en-tête `Retry-After` |

## Étapes suivantes

- [Référence complète de l'API](https://docs.reservesalles.example/reference)
- [Webhooks](https://docs.reservesalles.example/webhooks) pour être notifié d'une réservation ou d'une annulation
- [Gestion des fuseaux horaires](https://docs.reservesalles.example/fuseaux-horaires)
- [SDK officiels](https://docs.reservesalles.example/sdk) (Python, Node.js, Go)
