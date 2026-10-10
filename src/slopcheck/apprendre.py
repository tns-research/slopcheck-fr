"""`slopcheck learn` : transformer une phrase rejetée en règle.

La boucle reprend celle qu'un éditeur fait à la main : on écrit le motif, on
le passe sur un corpus humain pour mesurer les faux positifs, on règle la
sévérité, puis on l'ajoute à son pack personnel avec la phrase en exemple."""
import re
import unicodedata
from pathlib import Path

from .regles import Rule
from .segment import parse

DETERMINANTS = {"le", "la", "les", "un", "une", "des", "du", "de", "ce", "cet", "cette", "ces",
                "votre", "vos", "notre", "nos", "son", "sa", "ses", "leur", "leurs", "mon", "ma", "mes"}


def motif(phrase: str, souple: bool = True) -> str:
    """Motif regex tiré d'une phrase : apostrophes droites ou courbes,
    espaces souples, déterminants interchangeables."""
    jetons = re.findall(r"[\wÀ-ÿœ]+|['’]|[^\w\s]", phrase.strip().lower())
    out, prev = "", None
    for j in jetons:
        if j in ("'", "’"):
            kind, p = "apos", "['’]"
        elif re.match(r"[\wÀ-ÿœ]+$", j):
            kind = "w"
            p = ("(?:" + "|".join(sorted(DETERMINANTS, key=len, reverse=True)) + ")"
                 if souple and j in DETERMINANTS else re.escape(j))
        else:
            kind, p = "punct", re.escape(j)
        if prev:
            out += "" if "apos" in (kind, prev) else (r"\s+" if kind == prev == "w" else r"\s*")
        out += p
        prev = kind
    return r"\b" + out + (r"\b" if prev == "w" else "")


def slug(phrase: str) -> str:
    s = unicodedata.normalize("NFKD", phrase.lower()).encode("ascii", "ignore").decode()
    mots = re.findall(r"[a-z0-9]+", s)[:5]
    return "-".join(mots) or "regle-perso"


def mesure(pattern: str, fichiers) -> dict:
    r = Rule(id="candidat", severity="warn", pattern=pattern).compile()
    mots, hits, exemples = 0, 0, []
    for f in fichiers:
        doc = parse(str(f), Path(f).read_text(encoding="utf-8", errors="replace"))
        mots += doc.words
        for b in doc.blocks:
            for m in r.rx.finditer(b.text):
                hits += 1
                if len(exemples) < 5:
                    a = max(0, m.start() - 40)
                    exemples.append(f"{Path(f).name}:{b.line_at(m.start())}  …{' '.join(b.text[a:m.end() + 40].split())}…")
    taux = 1000 * hits / mots if mots else 0.0
    return {"mots": mots, "hits": hits, "taux": taux, "exemples": exemples}


def verdict(taux: float, hits: int) -> str:
    if hits == 0 or taux < 0.05:
        return "block"
    if taux < 0.3:
        return "warn"
    return "trop-large"


def _toml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def bloc_toml(rid, pattern, severity, message, fix, phrase) -> str:
    pat = f"'''{pattern}'''" if "'''" not in pattern and not pattern.endswith("'") else _toml_str(pattern)
    return (f"\n[[rule]]\nid = {_toml_str(rid)}\nfamily = \"perso\"\nseverity = {_toml_str(severity)}\n"
            f"pattern = {pat}\nmessage = {_toml_str(message)}\nfix = {_toml_str(fix)}\n"
            f"bad = [{_toml_str(phrase)}]\n")


def sauve(chemin: Path, bloc: str):
    if not chemin.exists():
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(f"[pack]\nname = {_toml_str(chemin.stem)}\ndescription = \"Règles personnelles\"\n",
                          encoding="utf-8")
    with chemin.open("a", encoding="utf-8") as fh:
        fh.write(bloc)
