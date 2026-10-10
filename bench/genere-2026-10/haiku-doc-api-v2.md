# Démarrage rapide

Ce guide vous permet d'obtenir vos premières prévisions météo depuis une application mobile en moins de 10 minutes.

## Prérequis

- Un compte développeur (créez-le sur le [tableau de bord](https://dashboard.meteo-api.example.com))
- Une clé d'API, disponible dans la section **Clés d'API** de votre tableau de bord
- Un environnement de développement mobile :
  - **iOS** : Xcode 15 ou plus récent, Swift 5.9 ou plus récent
  - **Android** : Android Studio Hedgehog ou plus récent, Kotlin 1.9 ou plus récent
  - **React Native** : Node.js 18 ou plus récent

> **Sécurité :** ne placez jamais votre clé d'API directement dans le code de l'application publiée. Toute personne qui décompile votre application pourrait l'extraire. Pour la production, passez par votre propre serveur (voir [Bonnes pratiques](#bonnes-pratiques)).

## 1. Testez votre clé avec curl

Avant d'écrire la moindre ligne de code d'application, vérifiez que votre clé fonctionne :

```bash
curl "https://api.meteo-api.example.com/v1/forecast?lat=48.8566&lon=2.3522&days=3" \
  -H "Authorization: Bearer VOTRE_CLE_API"
```

La réponse est un objet JSON de ce type :

```json
{
  "location": {
    "name": "Paris",
    "country": "FR",
    "lat": 48.8566,
    "lon": 2.3522,
    "timezone": "Europe/Paris"
  },
  "current": {
    "time": "2026-10-09T14:00:00+02:00",
    "temperature_c": 17.4,
    "feels_like_c": 16.8,
    "humidity_pct": 62,
    "wind_kmh": 14.2,
    "condition": "partly_cloudy",
    "is_day": true
  },
  "daily": [
    {
      "date": "2026-10-09",
      "temp_min_c": 11.0,
      "temp_max_c": 19.5,
      "precipitation_probability_pct": 20,
      "condition": "partly_cloudy"
    }
  ]
}
```

Si vous recevez une erreur `401 Unauthorized`, vérifiez que la clé est correcte et que l'en-tête `Authorization` est bien transmis.

## 2. Effectuez votre premier appel depuis l'application

Les exemples ci-dessous récupèrent les conditions actuelles pour une position donnée.

### iOS (Swift)

```swift
import Foundation

struct ForecastResponse: Decodable {
    let location: Location
    let current: Current

    struct Location: Decodable {
        let name: String
        let country: String
    }

    struct Current: Decodable {
        let temperatureC: Double
        let condition: String

        enum CodingKeys: String, CodingKey {
            case temperatureC = "temperature_c"
            case condition
        }
    }
}

func fetchCurrentWeather(lat: Double, lon: Double) async throws -> ForecastResponse {
    var components = URLComponents(string: "https://api.meteo-api.example.com/v1/forecast")!
    components.queryItems = [
        URLQueryItem(name: "lat", value: String(lat)),
        URLQueryItem(name: "lon", value: String(lon)),
        URLQueryItem(name: "days", value: "1")
    ]

    var request = URLRequest(url: components.url!)
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")

    let (data, response) = try await URLSession.shared.data(for: request)

    guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
        throw URLError(.badServerResponse)
    }

    return try JSONDecoder().decode(ForecastResponse.self, from: data)
}

// Utilisation
let weather = try await fetchCurrentWeather(lat: 48.8566, lon: 2.3522)
print("\(weather.location.name) : \(weather.current.temperatureC) °C")
```

### Android (Kotlin)

Ajoutez d'abord la dépendance Retrofit et le convertisseur Moshi (ou Gson) dans `build.gradle.kts` :

```kotlin
dependencies {
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-moshi:2.11.0")
}
```

Puis définissez le service et son appel :

```kotlin
import retrofit2.Retrofit
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Query
import com.squareup.moshi.Json
import com.squareup.moshi.Moshi
import retrofit2.converter.moshi.MoshiConverterFactory

data class ForecastResponse(
    val location: Location,
    val current: Current
)

data class Location(val name: String, val country: String)

data class Current(
    @Json(name = "temperature_c") val temperatureC: Double,
    val condition: String
)

interface WeatherService {
    @GET("v1/forecast")
    suspend fun getForecast(
        @Header("Authorization") auth: String,
        @Query("lat") lat: Double,
        @Query("lon") lon: Double,
        @Query("days") days: Int = 1
    ): ForecastResponse
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.meteo-api.example.com/")
    .addConverterFactory(MoshiConverterFactory.create(Moshi.Builder().build()))
    .build()

val weatherService = retrofit.create(WeatherService::class.java)

// Dans une coroutine
val weather = weatherService.getForecast(
    auth = "Bearer $apiKey",
    lat = 48.8566,
    lon = 2.3522
)
println("${weather.location.name} : ${weather.current.temperatureC} °C")
```

### React Native (TypeScript)

```typescript
type CurrentWeather = {
  location: { name: string; country: string };
  current: { temperature_c: number; condition: string };
};

export async function fetchCurrentWeather(
  lat: number,
  lon: number
): Promise<CurrentWeather> {
  const params = new URLSearchParams({
    lat: String(lat),
    lon: String(lon),
    days: '1',
  });

  const response = await fetch(
    `https://api.meteo-api.example.com/v1/forecast?${params}`,
    { headers: { Authorization: `Bearer ${API_KEY}` } }
  );

  if (!response.ok) {
    throw new Error(`Erreur API : ${response.status}`);
  }

  return response.json();
}

// Utilisation
const weather = await fetchCurrentWeather(48.8566, 2.3522);
console.log(`${weather.location.name} : ${weather.current.temperature_c} °C`);
```

## 3. Comprendre la réponse

| Champ | Type | Description |
|---|---|---|
| `location` | objet | Nom, pays, coordonnées et fuseau horaire du lieu |
| `current` | objet | Conditions actuelles (mises à jour toutes les 10 minutes) |
| `daily` | tableau | Prévisions journalières, une entrée par jour demandé |
| `current.condition` | chaîne | Code de condition (voir la [liste complète](#codes-de-condition)) |
| `*_c` | nombre | Température en degrés Celsius |
| `*_kmh` | nombre | Vitesse en kilomètres par heure |
| `*_pct` | nombre | Pourcentage, entre 0 et 100 |

Les unités sont en système métrique par défaut. Pour obtenir les unités impériales, ajoutez `units=imperial`.

## 4. Gérer les erreurs

L'API renvoie des codes HTTP standard, accompagnés d'un corps JSON explicite :

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Vous avez dépassé la limite de 1 000 requêtes par heure.",
    "retry_after_s": 1800
  }
}
```

| Code HTTP | Signification | Action recommandée |
|---|---|---|
| `400` | Paramètre invalide (latitude hors plage, par exemple) | Corrigez la requête |
| `401` | Clé d'API absente ou invalide | Vérifiez la clé |
| `429` | Limite de requêtes atteinte | Attendez `retry_after_s` secondes |
| `500`, `503` | Erreur serveur | Réessayez avec un délai croissant |

## Bonnes pratiques

- **Mettez les réponses en cache.** Les prévisions sont mises à jour au plus toutes les 10 minutes. Conservez-les localement pendant au moins 10 minutes avant de les redemander.
- **Ne demandez que ce dont vous avez besoin.** Passez `days=1` si vous n'affichez que la météo du jour.
- **Ne transmettez pas de position précise inutilement.** Arrondir les coordonnées à deux décimales suffit pour une prévision locale (environ 1 km).
- **Protégez votre clé.** Pour une application en production, faites transiter les appels par votre serveur, qui ajoute la clé côté serveur.

## Étapes suivantes

- [Référence des endpoints](https://docs.meteo-api.example.com/reference) : tous les paramètres disponibles
- [Alertes météo](https://docs.meteo-api.example.com/alerts) : recevez des notifications push en cas de vigilance
- [Historique](https://docs.meteo-api.example.com/history) : données passées pour vos analyses
- [SDK officiels](https://docs.meteo-api.example.com/sdks) : bibliothèques prêtes à l'emploi pour iOS, Android et React Native

## Codes de condition

| Code | Description |
|---|---|
| `clear` | Ciel dégagé |
| `partly_cloudy` | Partiellement nuageux |
| `cloudy` | Nuageux |
| `fog` | Brouillard |
| `drizzle` | Bruine |
| `rain` | Pluie |
| `snow` | Neige |
| `thunderstorm` | Orage |
