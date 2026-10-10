"""Applique un jeu de règles à un document et produit les constats."""
import re
from collections import Counter
from dataclasses import dataclass

from .segment import parse
from .verifs import CHECKS


@dataclass
class Constat:
    file: str
    line: int
    severity: str
    code: str
    excerpt: str
    fix: str
    message: str
    note: str = ""

    def as_dict(self):
        return {k: getattr(self, k) for k in ("file", "line", "severity", "code", "excerpt", "message", "fix", "note")}


def _supprime(doc, hit) -> bool:
    r = hit.rule
    if r.id in doc.disabled or (r.family and r.family in doc.disabled):
        return True
    codes = doc.ignored.get(hit.line)
    return bool(codes) and ("*" in codes or r.id in codes or (r.family and r.family in codes))


def analyse_doc(doc, rules) -> list[Constat]:
    hits = []
    for r in rules:
        fn = CHECKS.get(r.check)
        if fn is None:
            raise ValueError(f"règle {r.id} : vérification inconnue « {r.check} »")
        for h in fn(r, doc):
            if not _supprime(doc, h):
                hits.append(h)
    compte = Counter(h.rule.id for h in hits)
    out, vus = [], Counter()
    for h in hits:
        vus[h.rule.id] += 1
        if h.rule.max_per_doc and vus[h.rule.id] > h.rule.max_per_doc:
            continue
        r = h.rule
        sev = h.severity or r.severity
        note = h.note
        if r.escalate_at and compte[r.id] >= r.escalate_at and sev != "block":
            sev = "block"
            note = f"x{compte[r.id]} dans le texte : la tournure devient un réflexe"
        if r.max_per_doc and compte[r.id] > r.max_per_doc and vus[r.id] == r.max_per_doc:
            note = (note + " ; " if note else "") + f"{compte[r.id] - r.max_per_doc} autre(s) occurrence(s) non affichée(s)"
        out.append(Constat(doc.name, h.line, sev, r.id, h.excerpt, r.fix, r.message, note))
    return sorted(out, key=lambda c: (c.line, c.code))


def analyse(name: str, text: str, rules) -> tuple[list[Constat], int]:
    doc = parse(name, text)
    return analyse_doc(doc, rules), doc.words


def decoupe(text: str, mots: int):
    """Coupe un long texte en morceaux d'environ `mots` mots, aux frontières de paragraphes.
    Sert au banc d'essai : un roman entier ne se lit pas comme un article."""
    if mots <= 0:
        yield 1, text
        return
    paras = re.split(r"(\n\s*\n)", text)
    buf, n, debut, ligne = [], 0, 1, 1
    for p in paras:
        buf.append(p)
        ligne += p.count("\n")
        n += len(p.split())
        if n >= mots and not p.strip() == "":
            yield debut, "".join(buf)
            buf, n, debut = [], 0, ligne
    if "".join(buf).strip():
        yield debut, "".join(buf)
