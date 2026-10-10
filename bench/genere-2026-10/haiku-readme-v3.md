# PhotoSync Android

Script open source qui sauvegarde automatiquement les photos d'un téléphone Android sur un disque dur externe. Il se connecte au téléphone via ADB, copie uniquement les nouvelles photos et conserve l'arborescence d'origine.

## Fonctionnalités

- Sauvegarde incrémentale : seules les photos absentes du disque sont copiées.
- Conservation des dates de prise de vue et de l'arborescence (`DCIM/Camera`, `DCIM/Screenshots`, etc.).
- Vérification d'intégrité (taille et hash SHA-256) après chaque copie.
- Lancement automatique à la connexion du téléphone (règle udev sous Linux, tâche planifiée sous Windows, `launchd` sous macOS).
- Journal détaillé et notification de fin de sauvegarde.
- Aucune installation d'application sur le téléphone, aucun compte cloud.

## Prérequis

- Python 3.9 ou supérieur
- [Android Debug Bridge (ADB)](https://developer.android.com/tools/adb) installé et accessible dans le `PATH`
- Un disque dur externe formaté en ext4, exFAT ou NTFS
- Un téléphone Android avec le **débogage USB** activé :
  1. Réglages → À propos du téléphone → appuyer 7 fois sur « Numéro de build ».
  2. Réglages → Options pour les développeurs → activer « Débogage USB ».
  3. Accepter l'empreinte RSA lors de la première connexion.

## Installation

```bash
git clone https://github.com/votre-compte/photosync-android.git
cd photosync-android
pip install -r requirements.txt
cp config.example.toml config.toml
```

## Configuration

Éditez `config.toml` :

```toml
[source]
# Dossiers du téléphone à sauvegarder
dossiers = ["/sdcard/DCIM/Camera", "/sdcard/Pictures/Screenshots"]
# Extensions prises en compte
extensions = [".jpg", ".jpeg", ".png", ".heic", ".mp4", ".mov"]

[destination]
# Point de montage du disque externe
chemin = "/media/utilisateur/Photos"
# Sous-dossier créé sur le disque
sous_dossier = "Telephone"

[options]
# Supprimer les fichiers du téléphone après sauvegarde (désactivé par défaut)
supprimer_apres_copie = false
# Nombre de copies simultanées
parallelisme = 2
# Notification à la fin (true/false)
notifications = true
```

> **Attention** : l'option `supprimer_apres_copie` efface des fichiers sur le téléphone. Ne l'activez qu'après avoir vérifié plusieurs sauvegardes complètes.

## Utilisation

Sauvegarde manuelle :

```bash
python photosync.py
```

Options courantes :

```bash
python photosync.py --config autre_config.toml   # fichier de configuration alternatif
python photosync.py --dry-run                    # affiche ce qui serait copié, sans rien écrire
python photosync.py --verbose                    # journal détaillé
python photosync.py --reset-index                # reconstruit l'index des fichiers déjà sauvegardés
```

Un fichier `.photosync_index.json` est créé à la racine de la destination. Il sert à éviter de recopier les fichiers déjà sauvegardés. Ne le supprimez pas sans raison.

## Lancement automatique

### Linux (udev)

Copiez la règle fournie dans `contrib/99-photosync.rules` vers `/etc/udev/rules.d/`, puis rechargez udev :

```bash
sudo cp contrib/99-photosync.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

Le script se lance dès que le téléphone est détecté en ADB.

### Windows

Créez une tâche planifiée déclenchée par l'événement « appareil connecté » et pointez-la vers `contrib/photosync.bat`.

### macOS

Chargez l'agent fourni dans `contrib/com.photosync.plist` :

```bash
cp contrib/com.photosync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.photosync.plist
```

## Structure du projet

```
photosync-android/
├── photosync.py          # Point d'entrée
├── photosync/
│   ├── adb.py            # Communication avec le téléphone
│   ├── copie.py          # Copie, vérification et index
│   ├── config.py         # Lecture de config.toml
│   └── notifications.py  # Notifications système
├── contrib/              # Règles udev, tâche Windows, agent launchd
├── tests/                # Tests unitaires
├── config.example.toml
└── requirements.txt
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Dépannage

| Problème | Solution |
|---|---|
| `adb: command not found` | Installez ADB et vérifiez le `PATH`. |
| `unauthorized` dans `adb devices` | Déverrouillez le téléphone et acceptez l'empreinte RSA. |
| `no devices/emulators found` | Changez de câble (certains ne transmettent que la charge) et vérifiez le mode USB « Transfert de fichiers ». |
| Disque non trouvé | Vérifiez `chemin` dans `config.toml` et que le disque est monté. |
| Copies lentes | Réduisez `parallelisme` à 1 ou utilisez un port USB 3.0. |

Pour un rapport de bug, joignez la sortie de `python photosync.py --verbose` (sans les noms de fichiers si vous le souhaitez).

## Contribuer

Les contributions sont les bienvenues. Ouvrez d'abord une issue pour discuter d'un changement important, puis envoyez une pull request. Merci de respecter le style du code existant et d'ajouter des tests pour les nouvelles fonctionnalités.

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE).
