# PDF Factures vers CSV

Un petit outil open source en ligne de commande pour extraire les données de factures PDF et les convertir en fichiers CSV.

## Fonctionnalités

- Conversion d’une facture PDF en CSV
- Traitement de plusieurs fichiers à la fois
- Extraction des champs courants : numéro, date, fournisseur, montant HT, TVA et total TTC
- Prise en charge des PDF contenant du texte
- Sortie compatible avec Excel, LibreOffice et les outils d’analyse de données

> Les PDF issus d’un scan nécessitent une étape d’OCR préalable.

## Installation

Prérequis : Python 3.10 ou version ultérieure.

```bash
git clone https://github.com/votre-compte/pdf-factures-csv.git
cd pdf-factures-csv
pip install .
```

## Utilisation

Convertir une facture :

```bash
factures-csv facture.pdf
```

Choisir le fichier de sortie :

```bash
factures-csv facture.pdf --sortie facture.csv
```

Convertir toutes les factures d’un dossier :

```bash
factures-csv factures/*.pdf --sortie factures.csv
```

Afficher toutes les options :

```bash
factures-csv --help
```

## Format de sortie

Le fichier CSV généré contient une ligne par facture :

```csv
fichier,numero,date,fournisseur,montant_ht,tva,total_ttc,devise
facture-001.pdf,F-2026-001,2026-01-15,Exemple SAS,100.00,20.00,120.00,EUR
```

Les dates utilisent le format ISO `AAAA-MM-JJ`. Les montants utilisent un point comme séparateur décimal.

## Limites

La structure des factures varie selon les fournisseurs. L’extraction peut nécessiter des ajustements pour certains modèles complexes ou atypiques. Vérifiez toujours les données générées avant leur utilisation comptable.

## Développement

Installez les dépendances de développement :

```bash
pip install -e ".[dev]"
```

Lancez les tests :

```bash
pytest
```

## Contribution

Les contributions sont les bienvenues. Avant de proposer une modification :

1. Créez une issue décrivant le problème ou l’amélioration.
2. Créez une branche dédiée.
3. Ajoutez ou mettez à jour les tests.
4. Ouvrez une pull request claire et concise.

N’incluez jamais de factures contenant des données personnelles ou confidentielles dans les issues, les tests ou les pull requests.

## Licence

Ce projet est distribué sous licence MIT. Consultez le fichier `LICENSE` pour plus d’informations.