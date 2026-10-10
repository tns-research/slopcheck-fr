"""Corpus humain de référence : textes du domaine public (Gutenberg) et
articles Wikipédia (CC BY-SA), téléchargés dans un cache local et jamais
redistribués avec le dépôt. Sert à mesurer le taux de faux positifs."""
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GUTENBERG = {
    4650: "voltaire-candide",
    13951: "dumas-trois-mousquetaires",
    14155: "flaubert-madame-bovary",
    17489: "hugo-miserables-1",
    2650: "proust-swann",
    5711: "zola-germinal",
    4791: "verne-centre-de-la-terre",
    13846: "descartes-methode",
}

WIKIPEDIA = [
    "Révolution_française", "Photosynthèse", "Victor_Hugo", "Marcel_Proust", "Tour_de_France",
    "Intelligence_artificielle", "Start-up", "Économie_de_la_France", "Bordeaux", "Fromage",
    "Jazz", "Château_de_Versailles", "Impressionnisme", "Sécurité_sociale_en_France", "Énergie_nucléaire",
    "Cinéma_français", "Agriculture_biologique", "Rugby_à_XV", "Marseille", "Mathématiques",
]

UA = {"User-Agent": "slopcheck-fr/0.1 (corpus de calibrage)"}


def default_dir() -> Path:
    env = os.environ.get("SLOPCHECK_CORPUS")
    if env:
        return Path(env)
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "slopcheck" / "corpus"


def _get(url: str, essais: int = 4) -> str:
    for i in range(essais):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == essais - 1:
                raise
            time.sleep(5 * (i + 1))


def _gutenberg_corps(t: str) -> str:
    debut = re.search(r"\*\*\* ?START OF.*?\*\*\*", t)
    fin = re.search(r"\*\*\* ?END OF", t)
    return t[debut.end() if debut else 0: fin.start() if fin else len(t)].strip()


def fetch(dest: Path | None = None, log=print) -> Path:
    dest = dest or default_dir()
    (dest / "gutenberg").mkdir(parents=True, exist_ok=True)
    (dest / "wikipedia").mkdir(parents=True, exist_ok=True)
    for gid, nom in GUTENBERG.items():
        f = dest / "gutenberg" / f"{nom}.txt"
        if f.exists():
            continue
        try:
            t = _get(f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt")
            f.write_text(_gutenberg_corps(t), encoding="utf-8")
            log(f"gutenberg  {nom}")
        except Exception as e:
            log(f"échec      {nom} : {e}")
    for titre in WIKIPEDIA:
        f = dest / "wikipedia" / f"{titre}.txt"
        if f.exists():
            continue
        url = ("https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&titles="
               + urllib.parse.quote(titre))
        try:
            pages = json.loads(_get(url))["query"]["pages"]
            texte = next(iter(pages.values())).get("extract", "")
            texte = re.sub(r"^=+ (.*?) =+$", lambda m: "## " + m.group(1), texte, flags=re.M)
            f.write_text(texte, encoding="utf-8")
            log(f"wikipedia  {titre}")
            time.sleep(1)
        except Exception as e:
            log(f"échec      {titre} : {e}")
    (dest / "LISEZMOI.md").write_text(
        "Corpus de calibrage de slopcheck. Gutenberg : domaine public. Wikipédia : CC BY-SA 4.0, "
        "contributeurs de fr.wikipedia.org. Usage local uniquement, ne pas redistribuer sans attribution.\n",
        encoding="utf-8")
    return dest


def files(paths) -> list[Path]:
    out = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            out += sorted(x for x in p.rglob("*") if x.suffix in (".md", ".txt", ".markdown") and x.is_file()
                          and x.name != "LISEZMOI.md")
        elif p.is_file():
            out.append(p)
    return out
