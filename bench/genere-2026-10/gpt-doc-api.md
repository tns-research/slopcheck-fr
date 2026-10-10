# Démarrage rapide

Ce guide vous accompagne dans la création de votre premier paiement avec l’API REST.

## Prérequis

Vous aurez besoin de votre clé API secrète, disponible depuis le tableau de bord.

> Ne partagez jamais votre clé secrète et ne l’intégrez pas dans du code exécuté côté client.

Dans votre terminal, définissez-la comme variable d’environnement :

```bash
export PAYMENT_API_KEY="sk_test_votre_cle"
```

## 1. Créer un paiement

Envoyez une requête `POST` vers `/v1/payments` :

```bash
curl --request POST \
  --url https://api.example.com/v1/payments \
  --header "Authorization: Bearer $PAYMENT_API_KEY" \
  --header "Content-Type: application/json" \
  --header "Idempotency-Key: commande-12345" \
  --data '{
    "amount": 2500,
    "currency": "EUR",
    "description": "Commande n°12345",
    "customer": {
      "email": "client@example.com"
    },
    "return_url": "https://votre-site.fr/paiement/termine"
  }'
```

Le montant est exprimé dans la plus petite unité de la devise : `2500` correspond à `25,00 EUR`.

### Réponse

```json
{
  "id": "pay_01J9ABCDEF",
  "status": "pending",
  "amount": 2500,
  "currency": "EUR",
  "checkout_url": "https://checkout.example.com/pay/pay_01J9ABCDEF",
  "created_at": "2026-10-09T12:00:00Z"
}
```

Redirigez le client vers `checkout_url` afin qu’il finalise le paiement.

## 2. Vérifier le paiement

Après le retour du client, récupérez l’état du paiement depuis votre serveur :

```bash
curl --request GET \
  --url https://api.example.com/v1/payments/pay_01J9ABCDEF \
  --header "Authorization: Bearer $PAYMENT_API_KEY"
```

Exemple de réponse après confirmation :

```json
{
  "id": "pay_01J9ABCDEF",
  "status": "succeeded",
  "amount": 2500,
  "currency": "EUR",
  "created_at": "2026-10-09T12:00:00Z"
}
```

Les principaux états sont :

| État | Description |
|---|---|
| `pending` | Le paiement attend une action du client. |
| `processing` | Le paiement est en cours de traitement. |
| `succeeded` | Le paiement a été confirmé. |
| `failed` | Le paiement a échoué. |
| `canceled` | Le paiement a été annulé. |

## 3. Recevoir les notifications

Configurez un webhook pour être averti des changements d’état, même si le client ne revient pas sur votre site.

```http
POST /webhooks/payment
Content-Type: application/json
X-Webhook-Signature: t=1791547200,v1=…

{
  "id": "evt_01J9XYZ",
  "type": "payment.succeeded",
  "created_at": "2026-10-09T12:01:08Z",
  "data": {
    "payment_id": "pay_01J9ABCDEF",
    "amount": 2500,
    "currency": "EUR"
  }
}
```

Vérifiez toujours la signature du webhook avec votre secret de signature avant de traiter l’événement. Votre endpoint doit répondre avec un code HTTP `2xx`.

## Idempotence

Ajoutez un en-tête `Idempotency-Key` unique à chaque tentative de création. Si une requête est renvoyée après une interruption réseau, la même clé empêche la création de paiements en double.

```http
Idempotency-Key: commande-12345
```

## Gestion des erreurs

Les erreurs utilisent des codes HTTP standards et renvoient un corps JSON structuré :

```json
{
  "error": {
    "type": "invalid_request",
    "code": "invalid_amount",
    "message": "Le montant doit être supérieur à zéro.",
    "request_id": "req_01J9ERROR"
  }
}
```

| Code HTTP | Signification |
|---|---|
| `400` | Requête invalide |
| `401` | Clé API absente ou incorrecte |
| `404` | Ressource introuvable |
| `409` | Conflit ou clé d’idempotence réutilisée avec d’autres paramètres |
| `429` | Trop de requêtes |
| `500` | Erreur temporaire du serveur |

Pour les erreurs `429` et `5xx`, réessayez avec un délai exponentiel. Conservez le même en-tête `Idempotency-Key`.

## Passer en production

Avant d’accepter de vrais paiements :

1. Remplacez votre clé de test `sk_test_…` par une clé de production `sk_live_…`.
2. Utilisez uniquement des URL HTTPS.
3. Configurez et vérifiez les signatures de webhook.
4. Ne considérez une commande comme payée qu’après avoir obtenu l’état `succeeded` depuis l’API ou un webhook vérifié.
5. Stockez vos clés dans un gestionnaire de secrets, jamais dans votre dépôt de code.