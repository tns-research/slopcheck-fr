"""Chargement des packs de règles (TOML) et de la configuration utilisateur.

Un pack est un fichier TOML :

    [pack]
    name = "mon-pack"
    extends = ["fr-signatures"]

    [[rule]]
    id = "mon-tic"
    severity = "block"
    pattern = '''\\bau final\\b'''
    message = "..."
    fix = "..."
    bad = ["Au final, on a gagné."]
    good = ["Le score final."]

Une règle qui reprend l'id d'une règle déjà chargée la modifie champ par
champ. `params_add` ajoute des valeurs aux listes de paramètres d'une règle
intégrée sans la recopier.
"""
import os
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

PACKS_DIR = Path(__file__).parent / "packs"
DEFAULT_PACKS = ["fr-signatures", "typo-fr"]
SEVERITIES = ("block", "warn", "off")
SCOPES = ("block", "sentence", "first_sentence", "last_sentence", "title", "raw")
CONFIG_NAMES = (".slopcheck.toml", "slopcheck.toml")


class ErreurConfig(Exception):
    pass


@dataclass
class Rule:
    id: str
    severity: str = "warn"
    message: str = ""
    fix: str = ""
    family: str = ""
    check: str = "regex"
    pattern: str = ""
    unless: str = ""
    flags: str = "i"
    scope: str = "block"
    kinds: tuple = ("paragraph", "list", "quote", "heading")
    max_per_block: int = 1
    max_per_doc: int = 0
    min_sentences: int = 2
    escalate_at: int = 0
    params: dict = field(default_factory=dict)
    bad: list = field(default_factory=list)
    good: list = field(default_factory=list)
    pack: str = ""
    rx: re.Pattern | None = None
    rx_unless: re.Pattern | None = None

    def compile(self):
        fl = 0
        if "i" in self.flags:
            fl |= re.I
        try:
            self.rx = re.compile(self.pattern, fl) if self.pattern else None
            self.rx_unless = re.compile(self.unless, fl) if self.unless else None
        except re.error as e:
            raise ErreurConfig(f"règle {self.id} (pack {self.pack}) : motif invalide : {e}")
        if self.severity not in SEVERITIES:
            raise ErreurConfig(f"règle {self.id} : sévérité inconnue « {self.severity} »")
        if self.scope not in SCOPES:
            raise ErreurConfig(f"règle {self.id} : portée inconnue « {self.scope} »")
        return self


CHAMPS = set(Rule.__dataclass_fields__) - {"rx", "rx_unless"}


def _merge(old: dict, new: dict):
    for k, v in new.items():
        if k == "params":
            old.setdefault("params", {}).update(v)
        elif k == "params_add":
            p = old.setdefault("params", {})
            for pk, pv in v.items():
                p[pk] = list(p.get(pk, [])) + list(pv)
        else:
            old[k] = v


def resolve_pack(ref: str, base: Path) -> Path:
    if ref.endswith(".toml") or "/" in ref or os.sep in ref:
        p = Path(os.path.expanduser(ref))
        return p if p.is_absolute() else (base / p).resolve()
    p = PACKS_DIR / f"{ref}.toml"
    if not p.exists():
        dispo = ", ".join(sorted(x.stem for x in PACKS_DIR.glob("*.toml")))
        raise ErreurConfig(f"pack inconnu « {ref} ». Packs fournis : {dispo}")
    return p


class RuleSet:
    def __init__(self):
        self.defs: dict[str, dict] = {}
        self.packs: list[str] = []
        self._vus: set = set()

    def load_file(self, path: Path, is_config: bool = False):
        path = path.resolve()
        if path in self._vus:
            return
        self._vus.add(path)
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise ErreurConfig(f"fichier introuvable : {path}")
        except tomllib.TOMLDecodeError as e:
            raise ErreurConfig(f"{path} : TOML invalide : {e}")
        meta = data.get("pack", {})
        parents = list(meta.get("extends", [])) + list(data.get("packs", []))
        if is_config and not parents:
            parents = list(DEFAULT_PACKS)
        for ref in parents:
            self.load_file(resolve_pack(ref, path.parent))
        nom = meta.get("name", path.stem)
        self.packs.append(nom)
        for r in data.get("rule", []):
            if "id" not in r:
                raise ErreurConfig(f"{path} : règle sans id")
            inconnus = set(r) - CHAMPS - {"params_add"}
            if inconnus:
                raise ErreurConfig(f"{path} : règle {r['id']} : champs inconnus {sorted(inconnus)}")
            if r["id"] in self.defs:
                _merge(self.defs[r["id"]], r)
            else:
                d = {"pack": nom}
                _merge(d, r)
                self.defs[r["id"]] = d
        self.apply_overrides(data)

    def apply_overrides(self, data: dict):
        for code in data.get("disable", []):
            self.set_severity(code, "off")
        for code, sev in data.get("severity", {}).items():
            self.set_severity(code, sev)
        for code, params in data.get("params_add", {}).items():
            if code in self.defs:
                _merge(self.defs[code], {"params_add": params})

    def set_severity(self, code: str, sev: str):
        touche = False
        for rid, d in self.defs.items():
            if rid == code or d.get("family") == code:
                d["severity"] = sev
                touche = True
        if not touche:
            raise ErreurConfig(f"aucune règle ni famille « {code} »")

    def rules(self, actives_only=True) -> list[Rule]:
        out = []
        for rid, d in self.defs.items():
            d = dict(d)
            for k in ("kinds",):
                if k in d:
                    d[k] = tuple(d[k])
            r = Rule(**{k: v for k, v in d.items() if k in CHAMPS}).compile()
            if actives_only and r.severity == "off":
                continue
            out.append(r)
        return out


def find_config(start: Path | None = None) -> Path | None:
    d = (start or Path.cwd()).resolve()
    for parent in [d, *d.parents]:
        for nom in CONFIG_NAMES:
            if (parent / nom).is_file():
                return parent / nom
    home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "slopcheck" / "config.toml"
    return home if home.is_file() else None


def load(config: str | None = None, packs: list[str] | None = None, no_config=False) -> RuleSet:
    rs = RuleSet()
    chemin = None if no_config else (Path(config) if config else find_config())
    if chemin:
        rs.load_file(chemin, is_config=True)
    else:
        for ref in DEFAULT_PACKS:
            rs.load_file(resolve_pack(ref, Path.cwd()))
    for ref in packs or []:
        rs.load_file(resolve_pack(ref, Path.cwd()))
    return rs


def all_builtin() -> RuleSet:
    rs = RuleSet()
    for p in sorted(PACKS_DIR.glob("*.toml")):
        rs.load_file(p)
    return rs
