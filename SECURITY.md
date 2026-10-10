# Sécurité

slopcheck lit des fichiers texte et n'envoie rien sur le réseau. Seule la commande `slopcheck corpus fetch` télécharge des textes, depuis gutenberg.org et fr.wikipedia.org, en HTTPS.

Les fichiers `.slopcheck.toml` et les packs de règles contiennent des expressions régulières. Une expression mal écrite peut ralentir fortement l'analyse : ne lancez pas slopcheck avec la configuration d'un dépôt auquel vous ne faites pas confiance, ou ajoutez `--no-config`.

Pour signaler une faille, utilisez l'onglet « Security » du dépôt GitHub (« Report a vulnerability ») plutôt qu'une issue publique.
