# factucsv

Convertit des factures PDF en fichier CSV, depuis la ligne de commande.

`factucsv` lit une ou plusieurs factures PDF (avec une couche texte, ou scannées via OCR) et en extrait les champs utiles : numéro, date, fournisseur, montants HT, TVA et TTC, ainsi que les lignes de détail. Le résultat est écrit dans un CSV prêt à être ouvert dans un tableur ou importé dans un logiciel de comptabilité.

## Installation

Python 3.10 ou plus récent est requis.

```bash
pipx install factucsv
```

Ou depuis les sources :

```bash
git clone https://github.com/exemple/factucsv.git
cd factucsv
pip install .
```

Pour traiter les PDF scannés, installez aussi [Tesseract](https://github.com/tesseract-ocr/tesseract) et son pack de langue française (`tesseract-ocr-fra` sous Debian/Ubuntu).

## Utilisation

Convertir une facture :

```bash
factucsv facture.pdf -o factures.csv
```

Convertir un dossier entier, en ajoutant les résultats à un CSV existant :

```bash
factucsv ./factures/ --recursif --ajouter -o compta.csv
```

Écrire sur la sortie standard, pour l'enchaîner avec d'autres outils :

```bash
factucsv facture.pdf | csvcut -c numero,total_ttc
```

### Options

| Option | Description |
|---|---|
| `-o, --sortie FICHIER` | Fichier CSV de sortie (par défaut : sortie standard) |
| `-r, --recursif` | Parcourt les sous-dossiers |
| `-a, --ajouter` | Ajoute au fichier de sortie au lieu de l'écraser |
| `--lignes` | Produit une ligne CSV par ligne de facture, et non une par facture |
| `--ocr` | Force l'OCR, même si le PDF contient du texte |
| `--separateur CAR` | Séparateur de colonnes (par défaut : `;`) |
| `--encodage ENC` | Encodage de sortie (par défaut : `utf-8`) |
| `--strict` | Quitte avec une erreur si un champ obligatoire est introuvable |
| `-v, --verbeux` | Affiche le détail du traitement |
| `--version` | Affiche la version |

## Format de sortie

Par défaut, une ligne par facture :

```csv
fichier;numero;date;fournisseur;siret;total_ht;tva;total_ttc;devise
facture-0412.pdf;F-2026-0412;2026-03-14;Atelier Dupont SARL;12345678900012;1250,00;250,00;1500,00;EUR
```

- Les dates sont au format ISO 8601 (`AAAA-MM-JJ`).
- Les montants utilisent la virgule décimale. Passez `--separateur ,` si vous préférez un CSV à l'anglo-saxonne : les montants utiliseront alors le point.
- Un champ introuvable est laissé vide, sauf avec `--strict`.

## Limites connues

- L'extraction repose sur des heuristiques de mise en page : les factures très atypiques peuvent donner des champs vides ou erronés. Relisez le résultat avant de l'importer en comptabilité.
- Les PDF protégés par mot de passe ne sont pas pris en charge.
- La qualité de l'OCR dépend de celle du scan (300 dpi recommandés).
- Les factures Factur-X / ZUGFeRD sont lues directement depuis le XML intégré quand il est présent, ce qui est plus fiable que l'extraction du texte.

## Contribuer

Les contributions sont les bienvenues.

1. Ouvrez une issue pour discuter du changement.
2. Créez une branche, puis une pull request.
3. Lancez les tests avant de proposer votre code :

```bash
pip install -e ".[dev]"
pytest
```

Si une facture n'est pas reconnue correctement, joignez à l'issue un exemple anonymisé (noms, IBAN et adresses masqués). C'est le meilleur moyen d'améliorer l'extraction.

## Licence

Distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE).
