# Démarrage rapide

Ce guide vous permet d'encaisser votre premier paiement de test en une quinzaine de minutes. Vous allez créer une clé d'API, envoyer une requête de paiement, puis recevoir la confirmation sur un webhook.

## Prérequis

- Un compte marchand (l'inscription est gratuite et donne accès au mode test).
- `curl`, ou un client HTTP de votre choix.
- Un serveur accessible en HTTPS pour recevoir les webhooks. En local, un tunnel comme `ngrok` suffit.

## 1. Récupérer vos clés d'API

Dans le tableau de bord, ouvrez **Développeurs › Clés d'API**. Chaque compte dispose de deux paires de clés :

| Clé | Préfixe | Usage |
|---|---|---|
| Clé secrète de test | `sk_test_` | Appels serveur en mode test |
| Clé publique de test | `pk_test_` | Intégration côté client (formulaire de carte) |
| Clé secrète de production | `sk_live_` | Appels serveur réels |
| Clé publique de production | `pk_live_` | Intégration côté client réelle |

> **Important :** la clé secrète donne un accès complet à votre compte. Ne la placez jamais dans du code côté client ni dans un dépôt Git. Stockez-la dans une variable d'environnement.

```bash
export PAY_API_KEY="sk_test_votre_cle"
```

## 2. Authentifier vos requêtes

L'URL de base de l'API est :

```
https://api.exemple.com/v1
```

Toutes les requêtes passent par HTTPS et s'authentifient avec un jeton Bearer :

```bash
curl https://api.exemple.com/v1/balance \
  -H "Authorization: Bearer $PAY_API_KEY"
```

Réponse attendue :

```json
{
  "object": "balance",
  "livemode": false,
  "available": [{ "amount": 0, "currency": "eur" }],
  "pending": [{ "amount": 0, "currency": "eur" }]
}
```

Si vous recevez une erreur `401`, vérifiez que la clé est complète et qu'elle commence bien par `sk_test_`.

## 3. Créer un paiement

Un paiement se crée avec `POST /payments`. Les montants s'expriment dans la plus petite unité de la devise : `2500` correspond à 25,00 €.

```bash
curl https://api.exemple.com/v1/payments \
  -H "Authorization: Bearer $PAY_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: commande-1042" \
  -d '{
    "amount": 2500,
    "currency": "eur",
    "description": "Commande n° 1042",
    "payment_method": "pm_card_visa",
    "confirm": true,
    "metadata": { "order_id": "1042" }
  }'
```

Réponse :

```json
{
  "id": "pay_1QxR8bK2eZvKYlo2",
  "object": "payment",
  "amount": 2500,
  "currency": "eur",
  "status": "succeeded",
  "description": "Commande n° 1042",
  "metadata": { "order_id": "1042" },
  "created": 1791561600,
  "livemode": false
}
```

L'en-tête `Idempotency-Key` évite de débiter deux fois le client si votre requête est rejouée après une coupure réseau. Utilisez une valeur unique par opération, par exemple l'identifiant de la commande.

### Exemples dans d'autres langages

**Node.js**

```javascript
const response = await fetch("https://api.exemple.com/v1/payments", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${process.env.PAY_API_KEY}`,
    "Content-Type": "application/json",
    "Idempotency-Key": "commande-1042",
  },
  body: JSON.stringify({
    amount: 2500,
    currency: "eur",
    payment_method: "pm_card_visa",
    confirm: true,
  }),
});

const payment = await response.json();
console.log(payment.id, payment.status);
```

**Python**

```python
import os
import requests

response = requests.post(
    "https://api.exemple.com/v1/payments",
    headers={
        "Authorization": f"Bearer {os.environ['PAY_API_KEY']}",
        "Idempotency-Key": "commande-1042",
    },
    json={
        "amount": 2500,
        "currency": "eur",
        "payment_method": "pm_card_visa",
        "confirm": True,
    },
    timeout=30,
)
response.raise_for_status()
payment = response.json()
print(payment["id"], payment["status"])
```

## 4. Tester différents scénarios

En mode test, aucune somme réelle n'est débitée. Les moyens de paiement suivants simulent les cas les plus courants :

| Moyen de paiement | Numéro de carte | Résultat |
|---|---|---|
| `pm_card_visa` | 4242 4242 4242 4242 | Paiement accepté |
| `pm_card_3ds` | 4000 0027 6000 3184 | Authentification 3-D Secure requise |
| `pm_card_declined` | 4000 0000 0000 0002 | Paiement refusé (`card_declined`) |
| `pm_card_insufficient_funds` | 4000 0000 0000 9995 | Fonds insuffisants |

Pour les numéros de carte, utilisez n'importe quelle date d'expiration future et n'importe quel cryptogramme à trois chiffres.

## 5. Gérer l'authentification 3-D Secure

Lorsque la banque exige une authentification forte (DSP2), le paiement passe au statut `requires_action` et la réponse contient une URL de redirection :

```json
{
  "id": "pay_1QxR9cK2eZvKYlo3",
  "status": "requires_action",
  "next_action": {
    "type": "redirect_to_url",
    "redirect_to_url": {
      "url": "https://auth.exemple.com/3ds/pay_1QxR9cK2eZvKYlo3",
      "return_url": "https://votre-site.fr/paiement/retour"
    }
  }
}
```

Redirigez le client vers `next_action.redirect_to_url.url`. Une fois l'authentification terminée, il revient sur votre `return_url`. Ne considérez pas le paiement comme réussi à ce moment-là : attendez le webhook décrit à l'étape suivante.

## 6. Recevoir les webhooks

Les webhooks vous informent des changements de statut, y compris ceux qui surviennent hors de votre requête initiale (authentification 3-D Secure, litige, remboursement).

1. Dans **Développeurs › Webhooks**, ajoutez l'URL de votre point de terminaison, par exemple `https://votre-site.fr/webhooks/paiement`.
2. Abonnez-vous au moins aux événements `payment.succeeded` et `payment.failed`.
3. Copiez le secret de signature (préfixe `whsec_`).

Chaque événement est envoyé en `POST` avec un en-tête `Pay-Signature` :

```
Pay-Signature: t=1791561600,v1=5257a869e7ecebeda32affa62cdca3fa51cad7e77a0e56ff536d0ce8e108d8bd
```

La signature `v1` est un HMAC-SHA256 calculé avec votre secret sur la chaîne `{t}.{corps brut de la requête}`. Vérifiez-la systématiquement avant de traiter l'événement :

```javascript
import crypto from "node:crypto";
import express from "express";

const app = express();

app.post(
  "/webhooks/paiement",
  express.raw({ type: "application/json" }),
  (req, res) => {
    const header = req.get("Pay-Signature") ?? "";
    const parts = Object.fromEntries(header.split(",").map((p) => p.split("=")));

    const expected = crypto
      .createHmac("sha256", process.env.PAY_WEBHOOK_SECRET)
      .update(`${parts.t}.${req.body}`)
      .digest("hex");

    const valid =
      parts.v1 &&
      expected.length === parts.v1.length &&
      crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(parts.v1));

    // Rejette les signatures invalides et les événements de plus de 5 minutes
    if (!valid || Math.abs(Date.now() / 1000 - Number(parts.t)) > 300) {
      return res.sendStatus(400);
    }

    const event = JSON.parse(req.body);
    if (event.type === "payment.succeeded") {
      // Marquer la commande event.data.metadata.order_id comme payée
    }

    res.sendStatus(200);
  }
);

app.listen(3000);
```

Répondez avec un code `2xx` en moins de 10 secondes. En cas d'échec, l'événement est renvoyé pendant 72 heures selon un délai croissant. Un même événement pouvant arriver plusieurs fois, rendez votre traitement idempotent en vous appuyant sur `event.id`.

## 7. Gérer les erreurs

L'API utilise les codes HTTP standards et renvoie un objet `error` détaillé :

```json
{
  "error": {
    "type": "card_error",
    "code": "card_declined",
    "decline_code": "insufficient_funds",
    "message": "La carte a été refusée pour fonds insuffisants.",
    "payment_id": "pay_1QxRAdK2eZvKYlo4"
  }
}
```

| Code HTTP | Signification | Que faire |
|---|---|---|
| `400` | Paramètre manquant ou invalide | Corriger la requête |
| `401` | Clé d'API absente ou invalide | Vérifier l'en-tête `Authorization` |
| `402` | Paiement refusé | Afficher `message` au client et proposer un autre moyen de paiement |
| `404` | Ressource introuvable | Vérifier l'identifiant et le mode (test ou production) |
| `409` | Conflit de clé d'idempotence | Ne pas réutiliser une clé avec des paramètres différents |
| `429` | Trop de requêtes | Réessayer avec un délai exponentiel |
| `5xx` | Erreur de notre côté | Réessayer avec la même `Idempotency-Key` |

## 8. Passer en production

Avant d'accepter de vrais paiements :

- [ ] Finalisez la vérification de votre compte dans **Paramètres › Entreprise**.
- [ ] Remplacez `sk_test_` par votre clé `sk_live_` dans la configuration de production.
- [ ] Déclarez un webhook de production et son secret `whsec_` dédié.
- [ ] Vérifiez que votre logique métier repose sur les webhooks, et non sur la redirection de retour.
- [ ] Testez au moins un paiement réel de faible montant, puis remboursez-le.

## Pour aller plus loin

- [Référence de l'API](./reference.md) : tous les endpoints et leurs paramètres
- [Remboursements](./remboursements.md) : rembourser tout ou partie d'un paiement
- [Abonnements](./abonnements.md) : facturer de manière récurrente
- [Liste des événements webhook](./webhooks-evenements.md)
- [Bonnes pratiques de sécurité](./securite.md)
