# Android Photo Backup

Script open source permettant de sauvegarder automatiquement les photos et vidéos d’un téléphone Android sur un disque dur externe.

## Fonctionnalités

- Détection du téléphone via ADB
- Copie des photos et vidéos vers un disque externe
- Sauvegarde incrémentale : seuls les nouveaux fichiers sont transférés
- Conservation de l’arborescence d’origine
- Journalisation des opérations
- Vérification du disque de destination avant chaque sauvegarde
- Automatisation avec `cron` ou `systemd`

## Prérequis

- Linux ou macOS
- Un téléphone Android avec le débogage USB activé
- Un câble USB compatible avec le transfert de données
- `adb`
- `rsync`
- Un disque dur externe monté

### Installation des dépendances

Ubuntu ou Debian :

```bash
sudo apt update
sudo apt install adb rsync
```

Fedora :

```bash
sudo dnf install android-tools rsync
```

macOS avec Homebrew :

```bash
brew install android-platform-tools rsync
```

## Préparation du téléphone

1. Ouvrez **Paramètres > À propos du téléphone**.
2. Appuyez sept fois sur **Numéro de build**.
3. Ouvrez **Options pour les développeurs**.
4. Activez **Débogage USB**.
5. Branchez le téléphone à l’ordinateur.
6. Autorisez la connexion lorsque la demande apparaît sur le téléphone.

Vérifiez que l’appareil est reconnu :

```bash
adb devices
```

Son état doit être `device`, et non `unauthorized`.

## Installation

Clonez le dépôt :

```bash
git clone https://github.com/votre-utilisateur/android-photo-backup.git
cd android-photo-backup
```

Rendez le script exécutable :

```bash
chmod +x android-photo-backup.sh
```

## Configuration

Copiez le fichier de configuration fourni :

```bash
cp config.example.env config.env
```

Modifiez ensuite `config.env` :

```dotenv
# Dossiers Android à sauvegarder, séparés par des deux-points
ANDROID_SOURCES="/sdcard/DCIM:/sdcard/Pictures"

# Point de montage du disque externe
BACKUP_DISK="/media/utilisateur/Photos"

# Sous-dossier de destination
BACKUP_DIRECTORY="Sauvegarde-Android"

# Emplacement du journal
LOG_FILE="./android-photo-backup.log"
```

Le chemin final sera construit ainsi :

```text
/media/utilisateur/Photos/Sauvegarde-Android/
```

> Utilisez un point de montage stable pour éviter d’écrire accidentellement sur le disque interne lorsque le disque externe est absent.

## Utilisation

Lancez une sauvegarde :

```bash
./android-photo-backup.sh
```

Simulez l’opération sans copier de fichiers :

```bash
./android-photo-backup.sh --dry-run
```

Affichez l’aide :

```bash
./android-photo-backup.sh --help
```

## Automatisation

### Avec cron

Ouvrez votre crontab :

```bash
crontab -e
```

Ajoutez cette ligne pour lancer une sauvegarde toutes les heures :

```cron
0 * * * * /chemin/vers/android-photo-backup/android-photo-backup.sh
```

Le script quitte normalement sans effectuer de copie si le téléphone ou le disque externe n’est pas disponible.

### Avec systemd

Créez `~/.config/systemd/user/android-photo-backup.service` :

```ini
[Unit]
Description=Sauvegarde des photos Android

[Service]
Type=oneshot
WorkingDirectory=/chemin/vers/android-photo-backup
ExecStart=/chemin/vers/android-photo-backup/android-photo-backup.sh
```

Créez ensuite `~/.config/systemd/user/android-photo-backup.timer` :

```ini
[Unit]
Description=Sauvegarde périodique des photos Android

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
Persistent=true

[Install]
WantedBy=timers.target
```

Activez le minuteur :

```bash
systemctl --user daemon-reload
systemctl --user enable --now android-photo-backup.timer
```

Vérifiez son état :

```bash
systemctl --user status android-photo-backup.timer
```

## Structure de la sauvegarde

Exemple :

```text
Sauvegarde-Android/
├── DCIM/
│   ├── Camera/
│   └── Screenshots/
└── Pictures/
    ├── Instagram/
    └── WhatsApp/
```

Les fichiers déjà présents ne sont pas transférés de nouveau, sauf si leur contenu ou leur date de modification a changé.

## Journaux

Consultez le journal avec :

```bash
tail -f android-photo-backup.log
```

Chaque exécution indique notamment :

- l’appareil détecté ;
- la destination utilisée ;
- le nombre de fichiers transférés ;
- les éventuelles erreurs.

## Sécurité

- Le script ne supprime aucun fichier du téléphone.
- Vérifiez toujours la destination avec `--dry-run` avant la première sauvegarde.
- Ne stockez pas de secrets dans `config.env`.
- Ajoutez `config.env` à `.gitignore` si vous personnalisez sa configuration.
- Une sauvegarde unique ne remplace pas une stratégie comprenant plusieurs copies sur des supports distincts.

## Dépannage

### Le téléphone apparaît comme `unauthorized`

Débranchez puis rebranchez le téléphone et acceptez la demande d’autorisation RSA. Vous pouvez également révoquer les autorisations de débogage USB depuis les options pour les développeurs.

### Aucun appareil n’est détecté

Essayez :

```bash
adb kill-server
adb start-server
adb devices
```

Vérifiez également le câble USB et sélectionnez le mode **Transfert de fichiers** sur le téléphone.

### Le disque externe n’est pas trouvé

Vérifiez son point de montage :

```bash
lsblk
```

Sur macOS :

```bash
ls /Volumes
```

Mettez ensuite à jour `BACKUP_DISK` dans `config.env`.

### Permission refusée

Assurez-vous que le dossier de destination est accessible en écriture :

```bash
test -w "/chemin/vers/le/disque" && echo "Accessible" || echo "Non accessible"
```

## Contribution

Les contributions sont les bienvenues :

1. Créez un fork du projet.
2. Créez une branche :

   ```bash
   git checkout -b amelioration/ma-fonctionnalite
   ```

3. Effectuez vos modifications.
4. Testez le script avec `--dry-run`.
5. Ouvrez une pull request.

Merci de ne jamais inclure de photos personnelles, de journaux sensibles ou de fichiers de configuration privés dans les rapports de bug.

## Licence

Ce projet est distribué sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d’informations.