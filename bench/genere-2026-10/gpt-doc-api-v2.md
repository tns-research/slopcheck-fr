# Démarrage rapide

Intégrez les conditions météo actuelles à votre application mobile en quelques minutes.

## 1. Obtenir une clé API

Créez une clé depuis votre tableau de bord, puis stockez-la de manière sécurisée.

> Ne placez pas une clé secrète directement dans le code de votre application. En production, faites transiter les requêtes par votre serveur ou utilisez une clé publique restreinte.

## 2. Interroger la météo actuelle

Envoyez une requête `GET` avec des coordonnées géographiques :

```http
GET https://api.meteo.example/v1/current?lat=48.8566&lon=2.3522&units=metric&lang=fr
Authorization: Bearer VOTRE_CLE_API
Accept: application/json
```

Avec `curl` :

```bash
curl "https://api.meteo.example/v1/current?lat=48.8566&lon=2.3522&units=metric&lang=fr" \
  -H "Authorization: Bearer VOTRE_CLE_API" \
  -H "Accept: application/json"
```

### Paramètres

| Paramètre | Type | Description |
|---|---|---|
| `lat` | nombre | Latitude, comprise entre `-90` et `90`. |
| `lon` | nombre | Longitude, comprise entre `-180` et `180`. |
| `units` | chaîne | `metric`, `imperial` ou `standard`. |
| `lang` | chaîne | Langue des descriptions, par exemple `fr`. |

## 3. Lire la réponse

```json
{
  "location": {
    "name": "Paris",
    "country": "FR",
    "latitude": 48.8566,
    "longitude": 2.3522
  },
  "current": {
    "temperature": 18.4,
    "feels_like": 17.9,
    "condition": "partiellement nuageux",
    "humidity": 64,
    "wind_speed": 3.8,
    "icon": "partly-cloudy-day"
  },
  "observed_at": "2026-10-09T14:30:00Z"
}
```

Les dates sont exprimées au format ISO 8601 en UTC. Avec `units=metric`, les températures sont en degrés Celsius et la vitesse du vent en mètres par seconde.

## 4. Intégrer l’API dans une application mobile

### Swift

```swift
import Foundation

let coordinates = "lat=48.8566&lon=2.3522"
let url = URL(
    string: "https://api.meteo.example/v1/current?\(coordinates)&units=metric&lang=fr"
)!

var request = URLRequest(url: url)
request.setValue("Bearer VOTRE_CLE_API", forHTTPHeaderField: "Authorization")
request.setValue("application/json", forHTTPHeaderField: "Accept")

URLSession.shared.dataTask(with: request) { data, response, error in
    guard error == nil, let data else {
        print("Erreur réseau :", error?.localizedDescription ?? "inconnue")
        return
    }

    guard let httpResponse = response as? HTTPURLResponse,
          (200...299).contains(httpResponse.statusCode) else {
        print("Réponse HTTP invalide")
        return
    }

    do {
        let weather = try JSONDecoder().decode(WeatherResponse.self, from: data)
        print("\(weather.current.temperature) °C")
    } catch {
        print("Réponse illisible :", error)
    }
}.resume()

struct WeatherResponse: Decodable {
    let current: CurrentWeather
}

struct CurrentWeather: Decodable {
    let temperature: Double
    let condition: String
}
```

### Kotlin

```kotlin
val request = Request.Builder()
    .url(
        "https://api.meteo.example/v1/current" +
        "?lat=48.8566&lon=2.3522&units=metric&lang=fr"
    )
    .header("Authorization", "Bearer VOTRE_CLE_API")
    .header("Accept", "application/json")
    .build()

client.newCall(request).enqueue(object : Callback {
    override fun onFailure(call: Call, error: IOException) {
        Log.e("Weather", "Erreur réseau", error)
    }

    override fun onResponse(call: Call, response: Response) {
        response.use {
            if (!it.isSuccessful) {
                Log.e("Weather", "Erreur HTTP ${it.code}")
                return
            }

            val json = it.body?.string()
            Log.d("Weather", json.orEmpty())
        }
    }
})
```

L’exemple Kotlin utilise [OkHttp](https://square.github.io/okhttp/).

## Gestion des erreurs

Les erreurs utilisent une structure JSON uniforme :

```json
{
  "error": {
    "code": "invalid_coordinates",
    "message": "La latitude doit être comprise entre -90 et 90."
  }
}
```

| Statut | Signification |
|---|---|
| `400` | Paramètres invalides. |
| `401` | Clé API absente ou invalide. |
| `403` | Requête non autorisée pour cette clé. |
| `429` | Limite de requêtes dépassée. |
| `500` | Erreur temporaire du service. |

Pour les réponses `429` et `5xx`, appliquez une nouvelle tentative avec un délai exponentiel. Mettez également les réponses en cache afin de réduire la consommation de données et de batterie.

## Étape suivante

Utilisez l’endpoint de prévisions pour afficher les prochaines heures :

```http
GET /v1/forecast?lat=48.8566&lon=2.3522&hours=24&units=metric&lang=fr
```