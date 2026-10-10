# Démarrage rapide

Ce guide vous permet d'effectuer votre premier paiement de test en moins de 10 minutes. Vous créez un paiement, redirigez votre client vers la page de paiement, puis récupérez le résultat.

**URL de base** : `https://api.paiement.example/v1`

## Prérequis

- Un compte marchand avec accès au tableau de bord
- Un outil pour envoyer des requêtes HTTP (`curl`, Postman, Insomnia ou le client de votre langage)
- Un serveur accessible en HTTPS pour recevoir les notifications (facultatif à cette étape)

## 1. Récupérer vos clés API

Dans le tableau de bord, ouvrez **Développeurs → Clés API**. Vous disposez de deux paires de clés :

| Environnement | Préfixe de la clé secrète | Usage |
|---|---|---|
| Test | `sk_test_` | Développement et tests, aucun débit réel |
| Production | `sk_live_` | Paiements réels |

> **Important** : la clé secrète donne accès à toutes vos opérations. Ne la placez jamais dans du code côté client (navigateur, application mobile) ni dans un dépôt Git. Si elle est exposée, régénérez-la immédiatement depuis le tableau de bord.

Exportez la clé dans votre terminal pour les exemples de ce guide :

```bash
export PAY_SECRET_KEY="sk_test_votre_cle"
```

## 2. Vérifier la connexion

Appelez le point de terminaison `/ping` :

```bash
curl https://api.paiement.example/v1/ping \
  -H "Authorization: Bearer $PAY_SECRET_KEY"
```

Réponse attendue :

```json
{
  "status": "ok",
  "mode": "test",
  "merchant_id": "mch_8f3k2d9x"
}
```

Si la réponse contient `"mode": "test"`, votre clé est bien une clé de test.

## 3. Créer un paiement

Envoyez une requête `POST /payments`. Les montants sont exprimés en **centimes** (entiers) : `1500` représente 15,00 €.

```bash
curl https://api.paiement.example/v1/payments \
  -H "Authorization: Bearer $PAY_SECRET_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: commande-1042-tentative-1" \
  -d '{
    "amount": 1500,
    "currency": "EUR",
    "description": "Commande n° 1042",
    "customer_email": "client@example.com",
    "return_url": "https://www.votre-site.fr/commande/1042/retour"
  }'
```

Réponse :

```json
{
  "id": "pay_4Lx9qW2mZr",
  "status": "requires_action",
  "amount": 1500,
  "currency": "EUR",
  "redirect_url": "https://checkout.paiement.example/pay/pay_4Lx9qW2mZr",
  "created_at": "2026-10-09T10:24:31Z"
}
```

Le champ `Idempotency-Key` est facultatif, mais recommandé : si votre requête échoue à cause d'un problème réseau et que vous la renvoyez avec la même clé, aucun second paiement n'est créé. Utilisez une valeur unique par opération métier.

### Les statuts possibles

| Statut | Signification |
|---|---|
| `requires_action` | Le client doit finaliser le paiement sur `redirect_url` |
| `processing` | Le paiement est en cours de traitement par le réseau bancaire |
| `succeeded` | Paiement accepté et capturé |
| `failed` | Paiement refusé. Le détail figure dans le champ `failure_reason` |
| `canceled` | Paiement annulé par le marchand ou expiré après 30 minutes |

## 4. Rediriger le client

Redirigez votre client vers `redirect_url`. La page de paiement hébergée gère la saisie de la carte et l'authentification forte (3D Secure 2) si elle est requise.

En test, utilisez la carte suivante :

- Numéro : `4242 4242 4242 4242`
- Date : n'importe quelle date future
- Cryptogramme : n'importe quels 3 chiffres

Une fois le paiement terminé, le client revient sur votre `return_url`, avec le paramètre `?payment_id=pay_4Lx9qW2mZr`.

> **Ne vous fiez pas à la redirection seule** pour valider une commande. Le client peut fermer son navigateur avant le retour. Utilisez les notifications (étape suivante) comme source de vérité.

## 5. Recevoir les notifications (webhooks)

Dans **Développeurs → Webhooks**, ajoutez l'URL de votre serveur, par exemple `https://www.votre-site.fr/webhooks/paiement`. Chaque changement de statut déclenche une requête `POST` signée.

```json
{
  "id": "evt_9Tq2LmA7xe",
  "type": "payment.succeeded",
  "created_at": "2026-10-09T10:25:02Z",
  "data": {
    "id": "pay_4Lx9qW2mZr",
    "amount": 1500,
    "currency": "EUR"
  }
}
```

### Vérifier la signature

Chaque requête contient l'en-tête `Pay-Signature`. Vérifiez-la avant de traiter l'événement, pour vous assurer qu'il provient bien de notre plateforme. Le secret de signature est affiché dans le tableau de bord, à côté de chaque endpoint.

```javascript
import crypto from "node:crypto";

function verifierSignature(corpsBrut, entete, secret) {
  const attendue = crypto
    .createHmac("sha256", secret)
    .update(corpsBrut, "utf8")
    .digest("hex");
  return crypto.timingSafeEqual(Buffer.from(attendue), Buffer.from(entete));
}
```

Le corps doit être lu **tel quel**, sans passer par un parseur JSON avant la vérification.

Répondez `200 OK` le plus vite possible. Tout code de retour différent de `2xx` déclenche une nouvelle tentative, avec un délai croissant pendant 72 heures.

## Gérer les erreurs

L'API renvoie des codes HTTP standards et un corps d'erreur explicite :

```json
{
  "error": {
    "type": "invalid_request",
    "code": "amount_too_small",
    "message": "Le montant minimum est de 50 centimes.",
    "param": "amount"
  }
}
```

| Code HTTP | Type | Action recommandée |
|---|---|---|
| `400` | `invalid_request` | Corrigez la requête (voir `param`) |
| `401` | `authentication_error` | Vérifiez la clé API et son environnement |
| `404` | `not_found` | La ressource n'existe pas ou n'appartient pas à votre compte |
| `409` | `idempotency_conflict` | La clé d'idempotence a déjà été utilisée avec un corps différent |
| `429` | `rate_limit_error` | Attendez le délai indiqué dans l'en-tête `Retry-After` |
| `5xx` | `api_error` | Réessayez avec un délai exponentiel. Le même `Idempotency-Key` est sans risque |

## Passer en production

1. Remplacez `sk_test_` par votre clé `sk_live_`, stockée dans une variable d'environnement ou un gestionnaire de secrets.
2. Créez un endpoint de webhook en production et enregistrez son secret de signature.
3. Effectuez un paiement réel de faible montant, puis remboursez-le depuis le tableau de bord.
4. Activez les alertes sur le taux d'échec dans **Paramètres → Notifications**.

## Étapes suivantes

- [Référence complète de l'API](https://docs.paiement.example/api)
- [Paiements récurrents et abonnements](https://docs.paiement.example/abonnements)
- [Remboursements et litiges](https://docs.paiement.example/remboursements)
- [Bibliothèques officielles](https://docs.paiement.example/sdk) (Node.js, Python, PHP, Java)

Une question ? Contactez le support à **support@paiement.example**, avec l'identifiant du paiement (`pay_…`) et l'horodatage de la requête.
