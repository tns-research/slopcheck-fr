# Démarrage rapide

Cette page vous guide pour effectuer votre premier paiement avec l'API en moins de cinq minutes.

## Prérequis

- Un compte développeur actif
- `curl` ou le client HTTP de votre choix
- Une clé d'API de test (voir ci-dessous)

## 1. Obtenir vos clés d'API

Dans le tableau de bord, ouvrez **Développeurs → Clés d'API**. Vous y trouverez deux types de clés :

| Type | Préfixe | Usage |
|---|---|---|
| Test | `sk_test_` | Développement, aucun mouvement de fonds réel |
| Production | `sk_live_` | Paiements réels |

> **Important** : la clé secrète ne doit jamais apparaître dans du code côté client, un dépôt public ou des logs. En cas de fuite, révoquez-la immédiatement depuis le tableau de bord.

Stockez-la dans une variable d'environnement :

```bash
export API_KEY="sk_test_votre_cle"
```

## 2. Authentification

Toutes les requêtes utilisent l'authentification Bearer sur HTTPS :

```bash
curl https://api.example.com/v1/balance \
  -H "Authorization: Bearer $API_KEY"
```

URL de base : `https://api.example.com/v1`

Une réponse `200 OK` confirme que votre clé est valide. Une réponse `401 Unauthorized` indique une clé absente ou incorrecte.

## 3. Créer un client

```bash
curl https://api.example.com/v1/customers \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "marie.dupont@example.com",
    "name": "Marie Dupont"
  }'
```

Réponse :

```json
{
  "id": "cus_8f3kQ2mZ",
  "object": "customer",
  "email": "marie.dupont@example.com",
  "name": "Marie Dupont",
  "created": 1790000000
}
```

## 4. Créer un paiement

Les montants sont exprimés dans la **plus petite unité de la devise** (centimes pour l'euro) : `2500` correspond à 25,00 €.

```bash
curl https://api.example.com/v1/payments \
  -H "Authorization: Bearer $API_KEY" \
  -H "Idempotency-Key: 6b1f0c2e-5d1a-4c1e-9a53-0f2f7d9b8a11" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 2500,
    "currency": "eur",
    "customer": "cus_8f3kQ2mZ",
    "payment_method": "pm_card_visa",
    "description": "Commande n° 1042",
    "confirm": true
  }'
```

Réponse :

```json
{
  "id": "pay_1Nq7xT",
  "object": "payment",
  "amount": 2500,
  "currency": "eur",
  "status": "succeeded",
  "customer": "cus_8f3kQ2mZ",
  "created": 1790000100
}
```

### Idempotence

L'en-tête `Idempotency-Key` permet de relancer une requête en toute sécurité après une erreur réseau, sans créer de doublon. Utilisez une valeur unique (UUID v4) par opération.

### Statuts d'un paiement

| Statut | Description |
|---|---|
| `requires_action` | Une authentification du client (3D Secure) est nécessaire |
| `processing` | Le paiement est en cours de traitement |
| `succeeded` | Le paiement est réussi |
| `failed` | Le paiement a été refusé ou a échoué |

## 5. Tester avec les cartes de test

En mode test, utilisez ces méthodes de paiement :

| Méthode | Résultat |
|---|---|
| `pm_card_visa` | Paiement accepté |
| `pm_card_declined` | Refus générique |
| `pm_card_insufficient_funds` | Fonds insuffisants |
| `pm_card_3ds_required` | Déclenche l'authentification 3D Secure |

## 6. Recevoir les notifications (webhooks)

Ne vous fiez pas uniquement à la réponse de l'API pour confirmer un paiement : certains paiements aboutissent de manière asynchrone. Configurez un endpoint webhook dans **Développeurs → Webhooks**, puis abonnez-vous aux événements :

- `payment.succeeded`
- `payment.failed`
- `refund.created`

Exemple de notification :

```json
{
  "id": "evt_4tYp0aLs",
  "type": "payment.succeeded",
  "data": {
    "object": { "id": "pay_1Nq7xT", "amount": 2500, "currency": "eur" }
  }
}
```

Vérifiez toujours la signature de l'en-tête `X-Signature` (HMAC-SHA256 avec votre secret de webhook) avant de traiter l'événement, et répondez par un `2xx` sous 10 secondes. Sans réponse valide, la notification est renvoyée pendant 72 heures avec un délai croissant.

## 7. Rembourser un paiement

```bash
curl https://api.example.com/v1/refunds \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "payment": "pay_1Nq7xT",
    "amount": 1000
  }'
```

Si `amount` est omis, le remboursement porte sur la totalité du paiement.

## Gestion des erreurs

L'API utilise les codes HTTP standards. Le corps de l'erreur est toujours structuré ainsi :

```json
{
  "error": {
    "type": "card_error",
    "code": "card_declined",
    "message": "La carte a été refusée.",
    "request_id": "req_92kd01"
  }
}
```

| Code HTTP | Signification |
|---|---|
| `400` | Requête invalide (paramètre manquant ou mal formé) |
| `401` | Authentification échouée |
| `402` | Paiement refusé |
| `404` | Ressource introuvable |
| `409` | Conflit (clé d'idempotence réutilisée avec d'autres paramètres) |
| `429` | Trop de requêtes, réessayez avec un délai croissant |
| `5xx` | Erreur côté serveur, réessayez avec la même clé d'idempotence |

Communiquez le `request_id` au support en cas de problème.

## Passer en production

Avant de basculer, vérifiez les points suivants :

- [ ] Le compte est activé et vérifié (KYC)
- [ ] La clé `sk_live_` est stockée de façon sécurisée
- [ ] Les webhooks de production sont configurés et la signature est vérifiée
- [ ] Les erreurs `4xx` et `5xx` sont gérées, avec reprises idempotentes
- [ ] Le parcours complet a été testé avec toutes les cartes de test

## Étapes suivantes

- [Référence de l'API](#)
- [Guide 3D Secure](#)
- [Gestion des abonnements](#)
- [Bibliothèques clientes officielles](#)
- [Contacter le support](#)
