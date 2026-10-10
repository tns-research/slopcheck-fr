# facture2csv

Outil en ligne de commande qui extrait les données de factures PDF et les convertit en fichiers CSV.

Il lit les factures générées numériquement (pas les scans), repère les champs courants (numéro, date, fournisseur, montants, lignes d’articles) et produit un CSV que vous pouvez ouvrir dans un tableur ou importer dans votre outil de comptabilité.

## Fonctionnalités

- Conversion d’une facture ou d’un dossier entier en une seule commande
- Extraction des en-têtes (numéro, date, fournisseur, client, totaux HT, TVA et TTC)
- Extraction des lignes d’articles (désignation, quantité, prix unitaire, montant)
- Prise en charge des formats de date et de nombre français (`09/10/2026`, `1 234,56 €`)
- Choix du séparateur CSV et de l’encodage
- Modèles d’extraction personnalisables au format YAML pour les factures récalcitrantes

## Installation

Python 3.10 ou plus récent est requis.

```bash
pip install facture2csv
```

Depuis les sources :

```bash
git clone https://github.com/exemple/facture2csv.git
cd facture2csv
pip install .
```

## Utilisation

Convertir une facture :

```bash
facture2csv facture.pdf
```

Le fichier `facture.csv` est créé à côté du PDF.

Convertir tout un dossier et regrouper le résultat dans un seul fichier :

```bash
facture2csv factures/ -o recapitulatif.csv
```

Extraire les lignes d’articles plutôt que les en-têtes :

```bash
facture2csv facture.pdf --mode lignes
```

### Options

| Option | Description | Défaut |
|---|---|---|
| `-o`, `--output` | Fichier CSV de sortie | même nom que le PDF |
| `--mode` | `entetes` ou `lignes` | `entetes` |
| `--separateur` | Séparateur de colonnes | `;` |
| `--encodage` | Encodage du fichier de sortie | `utf-8` |
| `--modele` | Fichier YAML de règles d’extraction | aucun |
| `--recursif` | Parcourir les sous-dossiers | désactivé |
| `-v`, `--verbose` | Afficher le détail de l’extraction | désactivé |

Le séparateur par défaut est le point-virgule, pour que le fichier s’ouvre correctement dans Excel en version française. Utilisez `--separateur ,` si vous préférez la virgule.

## Exemple de sortie

```csv
fichier;numero;date;fournisseur;total_ht;tva;total_ttc
facture-001.pdf;F2026-0142;2026-09-15;Papeterie Martin;250,00;50,00;300,00
facture-002.pdf;2026/873;2026-09-22;Imprimerie du Port;1 080,00;216,00;1 296,00
```

Les dates sont toujours écrites au format ISO (`AAAA-MM-JJ`). Les montants gardent la virgule décimale ; ajoutez `--decimal .` pour obtenir un point.

## Modèles personnalisés

Si un fournisseur utilise une mise en page que l’outil ne reconnaît pas, décrivez-la dans un fichier YAML :

```yaml
fournisseur: Imprimerie du Port
champs:
  numero: "Facture n°\\s*(\\S+)"
  date: "Date\\s*:\\s*(\\d{2}/\\d{2}/\\d{4})"
  total_ttc: "Net à payer\\s*([\\d\\s]+,\\d{2})"
```

```bash
facture2csv factures/ --modele imprimerie-du-port.yaml
```

## Limites

- Les PDF scannés (images) ne sont pas pris en charge. Passez-les d’abord dans un outil d’OCR comme `ocrmypdf`.
- Les tableaux répartis sur plusieurs pages peuvent nécessiter un modèle personnalisé.
- Les champs non trouvés restent vides dans le CSV, et l’option `-v` indique lesquels.

## Contribuer

Les contributions sont bienvenues. Pour signaler une facture mal lue, ouvrez une issue en joignant si possible une version anonymisée du PDF.

```bash
pip install -e ".[dev]"
pytest
```

## Licence

Distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE).
