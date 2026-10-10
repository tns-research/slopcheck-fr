```markdown
# pdf2csv

**pdf2csv** est un outil en ligne de commande qui extrait les données de factures au format PDF et les exporte dans un fichier CSV exploitable dans un tableur ou un logiciel de comptabilité.

## Fonctionnalités

- Conversion d'un ou plusieurs fichiers PDF en CSV, en une seule commande
- Extraction des champs usuels : numéro de facture, date, émetteur, montant HT, TVA et montant TTC
- Traitement par lot d'un dossier entier
- Sortie CSV compatible Excel (encodage UTF-8 avec BOM, séparateur configurable)
- Aucune donnée envoyée sur Internet : tout le traitement se fait en local

## Prérequis

- Python 3.9 ou supérieur
- `pdftotext` (paquet `poppler-utils` sous Debian/Ubuntu, `poppler` avec Homebrew sous macOS)

## Installation

```bash
pip install pdf2csv
```

Ou depuis les sources :

```bash
git clone https://github.com/votre-compte/pdf2csv.git
cd pdf2csv
pip install .
```

## Utilisation

Convertir une facture :

```bash
pdf2csv facture.pdf -o factures.csv
```

Convertir tout un dossier :

```bash
pdf2csv ./factures/ -o factures.csv
```

Choisir le séparateur et ajouter les colonnes brutes :

```bash
pdf2csv ./factures/ -o factures.csv --separateur ";" --brut
```

### Options

| Option | Description | Défaut |
|---|---|---|
| `-o, --sortie` | Fichier CSV de sortie | `sortie.csv` |
| `--separateur` | Séparateur de colonnes | `,` |
| `--brut` | Ajoute le texte brut extrait de chaque facture | désactivé |
| `--ocr` | Active la reconnaissance optique (PDF scannés) | désactivé |
| `-v, --verbose` | Affiche le détail du traitement | désactivé |
| `-h, --aide` | Affiche l'aide | |

## Exemple

Entrée `facture_0042.pdf` :

```
Facture n° 2026-0042
Date : 03/09/2026
Émetteur : Atelier Dupont SARL
Montant HT : 1 250,00 €
TVA (20 %) : 250,00 €
Montant TTC : 1 500,00 €
```

Sortie `factures.csv` :

```csv
fichier,numero,date,emetteur,montant_ht,tva,montant_ttc
facture_0042.pdf,2026-0042,2026-09-03,Atelier Dupont SARL,1250.00,250.00,1500.00
```

## Limites connues

- Les PDF scannés nécessitent l'option `--ocr` et l'installation de `tesseract` (langue française).
- L'extraction repose sur des expressions régulières : les mises en page très inhabituelles peuvent demander un modèle personnalisé (voir `docs/modeles.md`).
- Les montants sont normalisés au format décimal avec un point ; les devises autres que l'euro ne sont pas encore détectées.

## Contribuer

Les contributions sont les bienvenues. Ouvrez une issue pour signaler un bug ou proposer une amélioration, puis une pull request depuis une branche dédiée. Merci d'ajouter un test et un exemple de facture anonymisée pour tout nouveau format pris en charge.

```bash
pip install -e ".[dev]"
pytest
```

## Licence

Distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE).
```
