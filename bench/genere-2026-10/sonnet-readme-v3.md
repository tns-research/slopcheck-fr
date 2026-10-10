# android-photo-backup

Sauvegarde automatique des photos et vidéos d'un téléphone Android vers un disque dur externe, via ADB. Chaque exécution ne copie que les fichiers nouveaux.

![Licence MIT](https://img.shields.io/badge/licence-MIT-green)
![Plateformes](https://img.shields.io/badge/plateformes-Linux%20%7C%20macOS-blue)

## Fonctionnalités

- Copie incrémentale : les fichiers déjà sauvegardés sont ignorés.
- Détection automatique du disque externe et du téléphone branchés.
- Classement par date (`AAAA/MM`) à partir de la date de prise de vue.
- Vérification d'intégrité par somme de contrôle après copie.
- Mode simulation (`--dry-run`) pour voir ce qui serait copié.
- Lancement automatique à la connexion du téléphone (règle udev ou `launchd`).
- Aucune donnée n'est supprimée sur le téléphone, sauf avec l'option explicite `--clean`.

## Prérequis

- Linux ou macOS
- [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools) (`adb`)
- Bash 4 ou plus, `rsync`, `sha256sum` (ou `shasum` sous macOS)
- Un câble USB et un téléphone avec le **débogage USB** activé

## Installation

```bash
git clone https://github.com/votre-compte/android-photo-backup.git
cd android-photo-backup
chmod +x photo-backup.sh
sudo ln -s "$PWD/photo-backup.sh" /usr/local/bin/photo-backup
```

## Préparer le téléphone

1. Ouvrez **Paramètres > À propos du téléphone** et appuyez sept fois sur **Numéro de build**.
2. Ouvrez **Paramètres > Options pour les développeurs** et activez **Débogage USB**.
3. Branchez le téléphone et acceptez l'empreinte RSA de l'ordinateur.
4. Vérifiez la connexion :

```bash
adb devices
```

Le téléphone doit apparaître avec l'état `device`.

## Utilisation

```bash
photo-backup --dest /media/utilisateur/MonDisque/Photos
```

Exemples :

```bash
# Simulation, sans rien copier
photo-backup --dest /mnt/backup --dry-run

# Sauvegarder aussi les captures d'écran et WhatsApp
photo-backup --dest /mnt/backup --source /sdcard/Pictures --source /sdcard/DCIM

# Libérer de la place sur le téléphone après vérification des copies
photo-backup --dest /mnt/backup --clean
```

### Options

| Option | Description | Défaut |
|---|---|---|
| `--dest <chemin>` | Dossier de destination sur le disque externe | obligatoire |
| `--source <chemin>` | Dossier à sauvegarder sur le téléphone (répétable) | `/sdcard/DCIM` |
| `--serial <id>` | Numéro de série, si plusieurs appareils sont branchés | auto |
| `--no-verify` | Désactive la vérification par somme de contrôle | désactivé |
| `--clean` | Supprime du téléphone les fichiers copiés et vérifiés | désactivé |
| `--dry-run` | Affiche les actions sans les exécuter | désactivé |
| `-v`, `--verbose` | Sortie détaillée | désactivé |
| `-h`, `--help` | Affiche l'aide | |

## Structure de la sauvegarde

```
Photos/
├── 2025/
│   ├── 07/
│   │   ├── IMG_20250714_101532.jpg
│   │   └── VID_20250720_183011.mp4
│   └── 08/
└── .backup-index
```

Le fichier `.backup-index` mémorise les fichiers déjà copiés. Ne le supprimez pas, sinon tout sera recopié (sans doublons, grâce à la vérification des sommes de contrôle).

## Automatisation

### Linux (udev)

Créez `/etc/udev/rules.d/99-photo-backup.rules` :

```
ACTION=="add", SUBSYSTEM=="usb", ENV{ID_VENDOR_ID}=="18d1", RUN+="/usr/local/bin/photo-backup --dest /mnt/backup/Photos"
```

Remplacez `18d1` par l'identifiant constructeur de votre téléphone (`lsusb`), puis rechargez les règles :

```bash
sudo udevadm control --reload-rules
```

### macOS (launchd) ou exécution planifiée

Une tâche `cron` suffit si vous préférez une sauvegarde périodique :

```cron
0 22 * * * /usr/local/bin/photo-backup --dest /Volumes/MonDisque/Photos
```

Si le téléphone ou le disque est absent, le script s'arrête proprement avec un code de retour non nul.

## Dépannage

| Problème | Solution |
|---|---|
| `no devices/emulators found` | Vérifiez le câble, le mode **Transfert de fichiers** et le débogage USB. |
| `unauthorized` | Déverrouillez le téléphone et acceptez l'autorisation de débogage. |
| `permission denied` sur le disque | Vérifiez le point de montage et les droits en écriture. |
| Plusieurs appareils détectés | Indiquez `--serial` (voir `adb devices`). |

## Contribuer

Les contributions sont bienvenues.

1. Forkez le dépôt.
2. Créez une branche : `git checkout -b ma-fonctionnalite`.
3. Lancez les tests : `./tests/run.sh`.
4. Ouvrez une pull request en décrivant le changement.

Pour signaler un bug, ouvrez une issue avec la sortie de `photo-backup --verbose` et votre version d'`adb`.

## Licence

Distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE).
