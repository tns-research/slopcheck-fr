````markdown
# PhotoSauve

Sauvegarde automatique des photos et vidéos d'un téléphone Android vers un disque dur externe.

PhotoSauve se connecte au téléphone via ADB, en USB ou en Wi-Fi, et copie uniquement les nouveaux fichiers. Les photos sont rangées par année et par mois. Chaque copie est vérifiée. Aucune application n'est à installer sur le téléphone et aucun service cloud n'est utilisé.

## Fonctionnalités

- **Sauvegarde incrémentale** : seuls les fichiers absents du disque sont copiés.
- **Classement automatique** par date de prise de vue (`AAAA/MM/`), lue dans les métadonnées EXIF quand elles existent.
- **Vérification d'intégrité** : la somme SHA-256 de chaque fichier est comparée après la copie.
- **Détection des doublons**, même quand le fichier a été renommé.
- **Déclenchement automatique** quand le disque externe ou le téléphone est branché (règle udev et service systemd).
- **Nettoyage du téléphone (optionnel)** : suppression des fichiers déjà sauvegardés et vérifiés, au-delà d'un âge que vous choisissez.
- **Mode simulation** (`--dry-run`) pour voir ce qui serait fait sans rien modifier.
- Journal détaillé de chaque sauvegarde.

## Prérequis

- Linux (testé sous Debian 12, Ubuntu 24.04 et Fedora 40) ou macOS 13 et versions suivantes
- `bash` 4 ou version supérieure
- [`adb`](https://developer.android.com/tools/adb) (Android Platform Tools)
- `exiftool` (optionnel, recommandé pour un classement par date de prise de vue fiable)
- Un téléphone Android 8 ou version supérieure avec le **débogage USB activé**

### Installation des dépendances

```bash
# Debian / Ubuntu
sudo apt install adb libimage-exiftool-perl

# Fedora
sudo dnf install android-tools perl-Image-ExifTool

# macOS (Homebrew)
brew install android-platform-tools exiftool
```

## Installation

```bash
git clone https://github.com/exemple/photosauve.git
cd photosauve
sudo make install
```

Le script est installé dans `/usr/local/bin/photosauve`. Un fichier de configuration d'exemple est copié dans `~/.config/photosauve/photosauve.conf`.

## Préparer le téléphone

1. Ouvrez **Paramètres → À propos du téléphone** et appuyez sept fois sur **Numéro de build** pour activer les options pour les développeurs.
2. Dans **Paramètres → Système → Options pour les développeurs**, activez **Débogage USB**.
3. Branchez le téléphone à l'ordinateur et acceptez la demande d'autorisation qui s'affiche sur le téléphone. Cochez « Toujours autoriser depuis cet ordinateur ».
4. Vérifiez la connexion :

```bash
adb devices
```

Le téléphone doit apparaître avec l'état `device`.

## Utilisation

### Sauvegarde manuelle

```bash
photosauve --destination /media/$USER/DisqueExterne/Photos
```

### Simulation

```bash
photosauve --dry-run
```

### Options

| Option | Description |
|---|---|
| `-d`, `--destination CHEMIN` | Dossier de destination sur le disque externe |
| `-s`, `--source CHEMIN` | Dossier à sauvegarder sur le téléphone (option répétable) |
| `-n`, `--dry-run` | Affiche les opérations sans les exécuter |
| `--appareil ID` | Choisit un téléphone précis quand plusieurs sont connectés (voir `adb devices`) |
| `--wifi IP[:PORT]` | Se connecte au téléphone en Wi-Fi |
| `--nettoyer JOURS` | Supprime du téléphone les fichiers sauvegardés et vérifiés depuis plus de `JOURS` jours |
| `--sans-tri` | Copie les fichiers sans les ranger par date |
| `-v`, `--verbeux` | Affiche plus de détails |
| `-h`, `--aide` | Affiche l'aide |

## Configuration

Les options peuvent être enregistrées dans `~/.config/photosauve/photosauve.conf` :

```bash
# Dossier de destination sur le disque externe
DESTINATION="/media/moi/DisqueExterne/Photos"

# Identifiant du disque (UUID), pour vérifier que c'est le bon disque qui est branché
# Pour le trouver : lsblk -o NAME,UUID,MOUNTPOINT
DISQUE_UUID="1234-ABCD"

# Dossiers à sauvegarder sur le téléphone
SOURCES=(
  "/sdcard/DCIM/Camera"
  "/sdcard/Pictures"
  "/sdcard/Movies"
)

# Extensions prises en compte
EXTENSIONS="jpg jpeg png heic webp dng mp4 mov"

# Supprimer du téléphone les fichiers sauvegardés depuis plus de N jours (0 = jamais)
NETTOYAGE_JOURS=0

# Fichier journal
JOURNAL="$HOME/.local/state/photosauve/photosauve.log"
```

Les options passées en ligne de commande remplacent celles du fichier de configuration.

## Sauvegarde automatique

Pour lancer la sauvegarde dès que le disque externe est branché :

```bash
photosauve --installer-auto
```

Cette commande installe :

- une règle udev qui détecte le disque grâce à son `DISQUE_UUID` ;
- un service systemd utilisateur, `photosauve.service`, qui démarre la sauvegarde si le téléphone est aussi connecté.

Commandes utiles :

```bash
systemctl --user status photosauve.service   # état du service
journalctl --user -u photosauve.service      # journaux
photosauve --desinstaller-auto               # désactiver la sauvegarde automatique
```

Vous pouvez aussi utiliser une tâche planifiée avec `cron`, par exemple tous les soirs à 21 h :

```cron
0 21 * * * /usr/local/bin/photosauve --wifi 192.168.1.42 >> ~/.local/state/photosauve/cron.log 2>&1
```

## Organisation des fichiers sauvegardés

```
Photos/
├── 2025/
│   ├── 11/
│   │   ├── IMG_20251103_142233.jpg
│   │   └── VID_20251115_093012.mp4
│   └── 12/
├── 2026/
│   └── 01/
└── .photosauve/
    ├── index.sha256     # empreintes des fichiers déjà sauvegardés
    └── derniere-sauvegarde
```

Ne supprimez pas le dossier `.photosauve/`. Il permet de détecter les doublons et de ne copier que les nouveaux fichiers.

## Sécurité des données

- Le script ne supprime **jamais** de fichier sur le téléphone sans l'option `--nettoyer` ou `NETTOYAGE_JOURS` explicitement réglée.
- Avant toute suppression, la somme SHA-256 de la copie présente sur le disque est recalculée et comparée à celle de l'original.
- Si le disque est plein, la sauvegarde s'arrête proprement. Les fichiers copiés partiellement sont effacés.
- Nous recommandons de tester d'abord avec `--dry-run`, puis de garder une seconde sauvegarde de vos photos (règle 3-2-1).

## Dépannage

**`adb devices` affiche `unauthorized`**
Débranchez puis rebranchez le téléphone, et acceptez la demande d'autorisation sur l'écran.

**Le téléphone n'est pas détecté**
Choisissez le mode USB « Transfert de fichiers » sur le téléphone et essayez un autre câble. Certains câbles ne servent qu'à la recharge.

**Les photos sont classées à la date du jour**
Installez `exiftool`. Sans lui, le script utilise la date de modification du fichier, qui est parfois fausse.

**Erreur `Permission denied` sur le disque**
Vérifiez que le disque est monté en écriture pour votre utilisateur. Les disques NTFS demandent parfois `ntfs-3g`.

## Contribuer

Les contributions sont les bienvenues.

1. Forkez le dépôt.
2. Créez une branche : `git checkout -b ma-fonctionnalite`.
3. Lancez les tests : `make test` (nécessite [bats](https://github.com/bats-core/bats-core)).
4. Ouvrez une pull request en décrivant votre modification.

Pour signaler un bug, ouvrez une issue en indiquant votre système, votre modèle de téléphone, votre version d'Android et le contenu du journal (lancé avec `--verbeux`).

## Licence

Distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE).
````
