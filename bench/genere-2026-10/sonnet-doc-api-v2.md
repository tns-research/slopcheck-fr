# Démarrage rapide

Cette page vous guide de la création de votre clé d'API jusqu'à l'affichage de la météo actuelle dans votre application iOS, Android ou React Native. Comptez environ 10 minutes.

## Prérequis

- Un compte développeur (gratuit, sans carte bancaire)
- Un projet mobile existant (iOS 15+, Android 8+ / API 26+, ou React Native 0.72+)
- Une connexion HTTPS sortante autorisée par votre application

## 1. Obtenir une clé d'API

1. Créez un compte sur le tableau de bord développeur.
2. Ouvrez **Projets**, puis **Nouveau projet**.
3. Copiez la clé générée depuis l'onglet **Clés d'API**.

Le plan gratuit inclut 1 000 requêtes par jour et 60 requêtes par minute.

> **Important :** n'intégrez jamais votre clé de production en clair dans le binaire de l'application. Elle peut être extraite d'un APK ou d'un IPA. Consultez la section [Sécuriser votre clé](#5-sécuriser-votre-clé).

## 2. Faire votre première requête

L'URL de base de l'API est :

```
https://api.meteo-exemple.com/v1
```

Testez d'abord avec `curl` pour vérifier que votre clé fonctionne :

```bash
curl "https://api.meteo-exemple.com/v1/current?lat=48.8566&lon=2.3522&units=metric&lang=fr" \
  -H "Authorization: Bearer VOTRE_CLE_API"
```

Réponse :

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
    "observed_at": "2026-10-09T14:00:00+02:00",
    "temperature": 17.4,
    "feels_like": 16.1,
    "humidity": 68,
    "wind_speed": 14.2,
    "wind_direction": 240,
    "pressure": 1013,
    "condition": {
      "code": "partly_cloudy",
      "label": "Partiellement nuageux",
      "icon_url": "https://cdn.meteo-exemple.com/icons/partly_cloudy.png"
    }
  }
}
```

### Paramètres courants

| Paramètre | Type | Description |
|-----------|------|-------------|
| `lat`, `lon` | nombre | Coordonnées GPS. Obligatoires si `q` est absent. |
| `q` | chaîne | Nom de ville (par exemple `Lyon,FR`), à la place des coordonnées. |
| `units` | chaîne | `metric` (par défaut), `imperial` ou `standard`. |
| `lang` | chaîne | Code de langue : `fr`, `en`, `es`, etc. |

## 3. Intégrer l'API dans votre application

### iOS (Swift)

```swift
import Foundation

struct WeatherResponse: Decodable {
    struct Current: Decodable {
        let temperature: Double
        let humidity: Int
        let condition: Condition
    }
    struct Condition: Decodable {
        let label: String
        let iconUrl: URL
    }
    let current: Current
}

func fetchWeather(lat: Double, lon: Double) async throws -> WeatherResponse {
    var components = URLComponents(string: "https://api.meteo-exemple.com/v1/current")!
    components.queryItems = [
        URLQueryItem(name: "lat", value: String(lat)),
        URLQueryItem(name: "lon", value: String(lon)),
        URLQueryItem(name: "lang", value: "fr")
    ]

    var request = URLRequest(url: components.url!)
    request.setValue("Bearer \(Config.apiKey)", forHTTPHeaderField: "Authorization")

    let (data, response) = try await URLSession.shared.data(for: request)
    guard (response as? HTTPURLResponse)?.statusCode == 200 else {
        throw URLError(.badServerResponse)
    }

    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    return try decoder.decode(WeatherResponse.self, from: data)
}
```

### Android (Kotlin, Retrofit)

Ajoutez les dépendances dans `build.gradle.kts` :

```kotlin
implementation("com.squareup.retrofit2:retrofit:2.11.0")
implementation("com.squareup.retrofit2:converter-moshi:2.11.0")
```

Déclarez le service :

```kotlin
interface WeatherService {
    @GET("current")
    suspend fun getCurrent(
        @Query("lat") lat: Double,
        @Query("lon") lon: Double,
        @Query("lang") lang: String = "fr"
    ): WeatherResponse
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.meteo-exemple.com/v1/")
    .client(
        OkHttpClient.Builder()
            .addInterceptor { chain ->
                chain.proceed(
                    chain.request().newBuilder()
                        .header("Authorization", "Bearer ${BuildConfig.WEATHER_API_KEY}")
                        .build()
                )
            }
            .build()
    )
    .addConverterFactory(MoshiConverterFactory.create())
    .build()

val service = retrofit.create(WeatherService::class.java)
```

### React Native (TypeScript)

```typescript
export async function fetchWeather(lat: number, lon: number) {
  const url = `https://api.meteo-exemple.com/v1/current?lat=${lat}&lon=${lon}&lang=fr`;

  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });

  if (!res.ok) {
    throw new Error(`Erreur API : ${res.status}`);
  }
  return res.json();
}
```

## 4. Explorer les autres endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /current` | Conditions actuelles |
| `GET /forecast/hourly` | Prévisions heure par heure sur 48 h |
| `GET /forecast/daily` | Prévisions quotidiennes sur 14 jours |
| `GET /alerts` | Alertes météo officielles (vigilance, orages, canicule) |
| `GET /air-quality` | Indice de qualité de l'air et polluants |
| `GET /geocode` | Recherche de lieux et autocomplétion |

## 5. Sécuriser votre clé

Pour une application en production :

- **Passez par votre propre backend.** Votre serveur appelle l'API météo et expose à l'application un endpoint restreint. La clé ne quitte jamais le serveur.
- **Ou utilisez des clés restreintes.** Dans le tableau de bord, limitez une clé à l'identifiant de bundle iOS (`com.exemple.monapp`) ou à l'empreinte de signature Android (SHA-256).
- **Stockez la clé hors du dépôt.** Utilisez un fichier `.xcconfig` ou `local.properties` ajouté à `.gitignore`.
- **Faites une rotation régulière.** Vous pouvez révoquer et régénérer une clé à tout moment sans interruption grâce aux clés secondaires.

## 6. Bonnes pratiques mobiles

- **Mettez les réponses en cache.** Les conditions actuelles sont mises à jour toutes les 10 minutes. Inutile d'interroger l'API plus souvent. Respectez l'en-tête `Cache-Control` renvoyé.
- **Limitez la fréquence de la localisation.** Ne relancez un appel que si l'utilisateur s'est déplacé de plus de 5 km.
- **Gérez le mode hors ligne.** Affichez la dernière réponse en cache avec l'heure d'observation (`observed_at`).
- **Économisez la batterie et les données.** Utilisez le paramètre `fields` pour ne demander que les champs utiles :
  `?fields=current.temperature,current.condition`
- **Utilisez la compression.** Envoyez `Accept-Encoding: gzip`. Les bibliothèques HTTP standard le font par défaut.

## 7. Gérer les erreurs

L'API renvoie des codes HTTP standards et un corps JSON explicite :

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Limite de 60 requêtes par minute atteinte.",
    "retry_after": 12
  }
}
```

| Code HTTP | `error.code` | Cause et action |
|-----------|--------------|-----------------|
| `400` | `invalid_parameter` | Paramètre manquant ou mal formé. Vérifiez la requête. |
| `401` | `invalid_api_key` | Clé absente, invalide ou révoquée. |
| `403` | `restricted_key` | La clé n'est pas autorisée pour cette application. |
| `404` | `location_not_found` | Lieu introuvable. Proposez une nouvelle recherche. |
| `429` | `rate_limit_exceeded` | Quota dépassé. Attendez `retry_after` secondes. |
| `5xx` | `server_error` | Erreur temporaire. Réessayez avec un délai exponentiel. |

Pour les erreurs `429` et `5xx`, appliquez un *backoff* exponentiel (1 s, 2 s, 4 s) avec un maximum de 3 tentatives.

## Étapes suivantes

- [Référence complète de l'API](#)
- [Notifications push pour les alertes météo](#)
- [Guide de migration du plan gratuit vers le plan Pro](#)
- [SDK officiels iOS et Android](#)
- [Exemples d'applications sur GitHub](#)

Une question ou un blocage ? Écrivez-nous à **support@meteo-exemple.com** ou rejoignez la communauté des développeurs sur le forum.
