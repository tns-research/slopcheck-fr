# Démarrage rapide

Ce guide vous permet d'afficher la météo actuelle dans votre application iOS ou Android en moins de dix minutes. Vous allez créer une clé d'API, envoyer une première requête puis intégrer l'appel dans votre code Swift ou Kotlin.

## Prérequis

- Un compte développeur sur le [tableau de bord](https://console.nimbus-meteo.example).
- iOS 15 ou version ultérieure (Swift 5.5 et plus), ou Android API 24 ou version ultérieure (Kotlin 1.8 et plus).
- Un outil pour tester des requêtes HTTP, comme `curl` ou Postman.

## 1. Obtenir une clé d'API

1. Connectez-vous au tableau de bord.
2. Ouvrez **Projets → Nouveau projet** et donnez un nom à votre application.
3. Dans l'onglet **Clés d'API**, cliquez sur **Générer une clé**.

Votre clé ressemble à ceci : `nmb_live_4f8a2c...`. Il existe aussi une clé de test (`nmb_test_...`). Elle renvoie des données fictives et ne compte pas dans votre quota.

> **⚠️ Sécurité :** une clé intégrée dans le binaire d'une application mobile peut être extraite en quelques minutes. En production, faites passer les appels par votre propre serveur, ou utilisez des jetons temporaires (voir [Authentification](./authentification.md)). Pour ce guide, une clé de test suffit.

## 2. Envoyer une première requête

Toutes les requêtes passent par l'URL de base suivante :

```
https://api.nimbus-meteo.example/v1
```

L'authentification se fait par l'en-tête `Authorization`. Récupérez la météo actuelle à Lyon :

```bash
curl "https://api.nimbus-meteo.example/v1/current?lat=45.764&lon=4.8357&units=metric&lang=fr" \
  -H "Authorization: Bearer nmb_test_VOTRE_CLE"
```

### Paramètres

| Paramètre | Type   | Obligatoire | Description                                              |
|-----------|--------|-------------|----------------------------------------------------------|
| `lat`     | nombre | oui         | Latitude, de -90 à 90                                    |
| `lon`     | nombre | oui         | Longitude, de -180 à 180                                 |
| `units`   | texte  | non         | `metric` (par défaut) ou `imperial`                      |
| `lang`    | texte  | non         | Langue des descriptions (`fr`, `en`, `es`…). Défaut : `en` |

### Réponse

```json
{
  "location": {
    "lat": 45.764,
    "lon": 4.8357,
    "name": "Lyon",
    "timezone": "Europe/Paris"
  },
  "current": {
    "time": "2026-10-09T14:00:00+02:00",
    "temperature": 17.4,
    "feels_like": 16.8,
    "humidity": 62,
    "wind_speed": 3.6,
    "condition": {
      "code": "partly_cloudy",
      "description": "Partiellement nuageux",
      "icon": "https://cdn.nimbus-meteo.example/icons/partly_cloudy.png"
    }
  }
}
```

Avec `units=metric`, les températures sont en °C et la vitesse du vent en m/s.

## 3. Intégrer l'appel dans votre application

### iOS (Swift)

```swift
import Foundation

struct WeatherResponse: Decodable {
    struct Current: Decodable {
        let temperature: Double
        let condition: Condition
    }
    struct Condition: Decodable {
        let code: String
        let description: String
    }
    let current: Current
}

enum WeatherError: Error {
    case invalidResponse(statusCode: Int)
}

func fetchCurrentWeather(lat: Double, lon: Double) async throws -> WeatherResponse {
    var components = URLComponents(string: "https://api.nimbus-meteo.example/v1/current")!
    components.queryItems = [
        URLQueryItem(name: "lat", value: String(lat)),
        URLQueryItem(name: "lon", value: String(lon)),
        URLQueryItem(name: "units", value: "metric"),
        URLQueryItem(name: "lang", value: "fr")
    ]

    var request = URLRequest(url: components.url!)
    request.setValue("Bearer \(APIConfig.key)", forHTTPHeaderField: "Authorization")

    let (data, response) = try await URLSession.shared.data(for: request)
    let statusCode = (response as? HTTPURLResponse)?.statusCode ?? 0
    guard statusCode == 200 else {
        throw WeatherError.invalidResponse(statusCode: statusCode)
    }
    return try JSONDecoder().decode(WeatherResponse.self, from: data)
}
```

Utilisation :

```swift
let weather = try await fetchCurrentWeather(lat: 45.764, lon: 4.8357)
print("\(weather.current.temperature) °C, \(weather.current.condition.description)")
```

### Android (Kotlin)

Ajoutez les dépendances dans `build.gradle.kts` :

```kotlin
dependencies {
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
}
```

N'oubliez pas la permission réseau dans `AndroidManifest.xml` :

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

Puis :

```kotlin
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import okhttp3.HttpUrl.Companion.toHttpUrl
import okhttp3.OkHttpClient
import okhttp3.Request

@Serializable
data class WeatherResponse(val current: Current)

@Serializable
data class Current(val temperature: Double, val condition: Condition)

@Serializable
data class Condition(val code: String, val description: String)

private val client = OkHttpClient()
private val json = Json { ignoreUnknownKeys = true }

suspend fun fetchCurrentWeather(lat: Double, lon: Double): WeatherResponse =
    withContext(Dispatchers.IO) {
        val url = "https://api.nimbus-meteo.example/v1/current".toHttpUrl().newBuilder()
            .addQueryParameter("lat", lat.toString())
            .addQueryParameter("lon", lon.toString())
            .addQueryParameter("units", "metric")
            .addQueryParameter("lang", "fr")
            .build()

        val request = Request.Builder()
            .url(url)
            .header("Authorization", "Bearer ${BuildConfig.NIMBUS_API_KEY}")
            .build()

        client.newCall(request).execute().use { response ->
            check(response.isSuccessful) { "Erreur HTTP ${response.code}" }
            json.decodeFromString<WeatherResponse>(response.body!!.string())
        }
    }
```

Utilisation depuis un `ViewModel` :

```kotlin
viewModelScope.launch {
    val weather = fetchCurrentWeather(45.764, 4.8357)
    _uiState.value = "${weather.current.temperature} °C, ${weather.current.condition.description}"
}
```

## 4. Obtenir les prévisions

L'endpoint `/forecast` renvoie les prévisions heure par heure (jusqu'à 48 h) et jour par jour (jusqu'à 10 jours). Il accepte les mêmes paramètres que `/current`, plus `days` :

```bash
curl "https://api.nimbus-meteo.example/v1/forecast?lat=45.764&lon=4.8357&days=5&lang=fr" \
  -H "Authorization: Bearer nmb_test_VOTRE_CLE"
```

Le détail des champs est décrit dans la [référence de l'endpoint `/forecast`](./reference/forecast.md).

## Codes d'erreur

| Code | Signification                     | Que faire                                                      |
|------|-----------------------------------|----------------------------------------------------------------|
| 400  | Paramètre manquant ou invalide    | Vérifiez `lat` et `lon`. Le champ `error.message` précise la cause. |
| 401  | Clé absente ou invalide           | Vérifiez l'en-tête `Authorization`.                            |
| 429  | Quota dépassé                     | Attendez le nombre de secondes indiqué par l'en-tête `Retry-After`. |
| 5xx  | Erreur côté serveur               | Réessayez avec un délai croissant (backoff exponentiel).       |

Exemple de réponse d'erreur :

```json
{
  "error": {
    "code": "invalid_parameter",
    "message": "Le paramètre 'lat' doit être compris entre -90 et 90."
  }
}
```

## Quotas

| Offre    | Requêtes par minute | Requêtes par mois |
|----------|---------------------|-------------------|
| Gratuite | 60                  | 100 000           |
| Pro      | 600                 | 5 000 000         |

Chaque réponse contient les en-têtes `X-RateLimit-Remaining` et `X-RateLimit-Reset`.

Les données météo actuelles sont mises à jour toutes les 10 minutes. Mettez les réponses en cache pendant cette durée : vos utilisateurs économisent de la batterie et des données mobiles, et vous économisez votre quota.

## Étapes suivantes

- [Authentification et jetons temporaires](./authentification.md) : sécuriser vos appels en production.
- [Alertes météo par notification push](./guides/alertes-push.md) : prévenir vos utilisateurs en cas d'orage ou de canicule.
- [Icônes et codes de condition](./reference/conditions.md) : la liste complète des valeurs de `condition.code`.
- [SDK officiels](./sdk.md) : des bibliothèques Swift Package Manager et Maven prêtes à l'emploi.
