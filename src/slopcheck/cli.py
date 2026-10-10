"""Interface en ligne de commande de slopcheck."""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from . import __version__, apprendre, corpus, regles
from .moteur import analyse, decoupe
from .regles import ErreurConfig

SOUS_COMMANDES = {"check", "rules", "test", "bench", "learn", "corpus", "init"}

INIT = """# Configuration slopcheck. Le fichier s'applique au dossier et à ses sous-dossiers.
# Packs chargés dans l'ordre ; une règle redéfinie plus bas l'emporte.
# Packs fournis : fr-signatures (défaut), typo-fr (défaut), fr-strict.
packs = ["fr-signatures", "typo-fr"]
# packs = ["fr-strict", "typo-fr", "./slopcheck-perso.toml"]

# Règles ou familles désactivées.
disable = []

# Sévérité par règle ou par famille : "block", "warn" ou "off".
[severity]
# "em-dash" = "block"

# Mots ajoutés aux listes d'une règle intégrée.
# [params_add.objet-agent]
# sujets_humains = ["kiné", "pharmacien"]
"""



def _gh_data(s: str) -> str:
    return s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _gh_prop(s: str) -> str:
    return _gh_data(s).replace(":", "%3A").replace(",", "%2C")

def _regles(args):
    rs = regles.load(args.config, (args.pack or []) + (["fr-strict"] if args.strict else []), args.no_config)
    return rs.rules()


def _ajoute_options_regles(p):
    p.add_argument("--config", help="fichier de configuration (défaut : .slopcheck.toml le plus proche)")
    p.add_argument("--pack", action="append", help="pack supplémentaire : nom fourni ou chemin .toml (répétable)")
    p.add_argument("--strict", action="store_true", help="raccourci pour --pack fr-strict")
    p.add_argument("--no-config", action="store_true", help="ignorer les fichiers de configuration")


def cmd_check(args) -> int:
    rules = _regles(args)
    tous, mots = [], 0
    for chemin in args.files:
        if chemin == "-":
            texte, nom = sys.stdin.read(), "<stdin>"
        else:
            try:
                texte, nom = Path(chemin).read_text(encoding="utf-8"), chemin
            except (OSError, UnicodeDecodeError) as e:
                print(f"slopcheck : {chemin} : {e}", file=sys.stderr)
                return 2
        constats, n = analyse(nom, texte, rules)
        tous += constats
        mots += n
    if args.min_severity == "block":
        tous = [c for c in tous if c.severity == "block"]
    blocks = sum(1 for c in tous if c.severity == "block")
    warns = len(tous) - blocks
    if args.format == "json":
        print(json.dumps({"blocks": blocks, "warns": warns, "words": mots,
                          "findings": [c.as_dict() for c in tous]}, ensure_ascii=False, indent=2))
    elif args.format == "github":
        for c in tous:
            niveau = "error" if c.severity == "block" else "warning"
            print(f"::{niveau} file={_gh_prop(c.file)},line={c.line},title={_gh_prop('slopcheck ' + c.code)}"
                  f"::{_gh_data(f'« {c.excerpt} » {c.fix}')}")
    elif args.summary:
        for (code, sev), n in Counter((c.code, c.severity) for c in tous).most_common():
            print(f"{n:5}  {sev.upper():5}  {code}")
        print(f"\n{blocks} BLOCK, {warns} WARN sur {mots} mots")
    else:
        for c in tous:
            note = f" ({c.note})" if c.note else ""
            print(f"{c.severity.upper():5} {c.file}:{c.line} [{c.code}] « {c.excerpt} »\n      -> {c.fix}{note}")
        print(f"\n{blocks} BLOCK, {warns} WARN sur {mots} mots")
    return 1 if blocks else 0


def cmd_rules(args) -> int:
    rs = regles.load(args.config, (args.pack or []) + (["fr-strict"] if args.strict else []), args.no_config)
    rules = rs.rules(actives_only=False)
    if args.code:
        r = next((r for r in rules if r.id == args.code), None)
        if not r:
            print(f"règle inconnue : {args.code}", file=sys.stderr)
            return 2
        print(f"{r.id}  [{r.severity.upper()}]  pack {r.pack}, famille {r.family or '-'}\n")
        print(f"{r.message}\nCorrection : {r.fix}")
        if r.escalate_at:
            print(f"Passe en BLOCK dès {r.escalate_at} occurrences dans le texte.")
        for b in r.bad:
            print(f"  ✗ {b}")
        for g in r.good:
            print(f"  ✓ {g}")
        return 0
    print(f"Packs chargés : {', '.join(rs.packs)}\n")
    for r in sorted(rules, key=lambda r: (r.family, r.id)):
        esc = f" (BLOCK dès {r.escalate_at})" if r.escalate_at and r.severity == "warn" else ""
        print(f"{r.severity.upper():5}  {r.id:26} {r.family:16} {r.message[:70]}{esc}")
    return 0


def _teste_regle(r, base_rules):
    from .moteur import analyse as an
    echecs = []
    seule = [x for x in base_rules if x.id == r.id]
    if seule and seule[0].severity == "off":
        return echecs
    for b in r.bad:
        if not any(c.code == r.id for c in an("<exemple>", b, seule)[0]):
            echecs.append(f"{r.id} : l'exemple fautif ne déclenche pas : {b!r}")
    for g in r.good:
        if any(c.code == r.id for c in an("<exemple>", g, seule)[0]):
            echecs.append(f"{r.id} : l'exemple correct déclenche : {g!r}")
    return echecs


def cmd_test(args) -> int:
    echecs, n = [], 0
    jeux = []
    for p in sorted(regles.PACKS_DIR.glob("*.toml")):
        rs = regles.RuleSet()
        rs.load_file(p)
        jeux.append(rs)
    if args.config or args.pack or regles.find_config():
        jeux.append(regles.load(args.config, args.pack, False))
    for rs in jeux:
        rules = rs.rules(actives_only=False)
        for r in rules:
            n += 1
            echecs += _teste_regle(r, rules)
    for e in dict.fromkeys(echecs):
        print("ÉCHEC", e)
    print(f"{n} règles testées, {len(set(echecs))} échec(s)")
    return 1 if echecs else 0


def cmd_bench(args) -> int:
    rules = _regles(args)
    chemins = args.paths or [str(corpus.default_dir())]
    fichiers = corpus.files(chemins)
    if not fichiers:
        print("Aucun fichier. Téléchargez le corpus de référence : slopcheck corpus fetch", file=sys.stderr)
        return 2
    mots, par_code, par_fichier = 0, Counter(), []
    for f in fichiers:
        texte = f.read_text(encoding="utf-8", errors="replace")
        m_f, b_f, a_f = 0, 0, 0
        for _, morceau in decoupe(texte, args.chunk):
            constats, n = analyse(str(f), morceau, rules)
            m_f += n
            a_f += len(constats)
            for c in constats:
                par_code[(c.code, c.severity)] += 1
                b_f += c.severity == "block"
        mots += m_f
        par_fichier.append((f.name, m_f, b_f, a_f))
    blocks = sum(n for (c, s), n in par_code.items() if s == "block")
    warns = sum(n for (c, s), n in par_code.items() if s == "warn")
    print(f"{len(fichiers)} fichiers, {mots} mots, découpage {args.chunk or 'aucun'}")
    print(f"BLOCK : {blocks} ({1000 * blocks / max(mots, 1):.2f} pour 1 000 mots)")
    print(f"WARN  : {warns} ({1000 * warns / max(mots, 1):.2f} pour 1 000 mots)")
    avec_b = sum(1 for x in par_fichier if x[2])
    avec_a = sum(1 for x in par_fichier if x[3])
    print(f"Fichiers avec au moins un BLOCK : {avec_b} sur {len(fichiers)}, avec au moins une alerte : {avec_a}\n")
    for (code, sev), n in par_code.most_common(args.top):
        print(f"{n:6}  {sev.upper():5}  {1000 * n / max(mots, 1):6.3f}/1000  {code}")
    if args.by_file:
        print()
        for nom, m, b, _ in par_fichier:
            print(f"{1000 * b / max(m, 1):6.2f}  {m:8} mots  {nom}")
    return 0


def cmd_learn(args) -> int:
    pattern = args.pattern or apprendre.motif(args.phrase, souple=not args.exact)
    try:
        r = regles.Rule(id="candidat", pattern=pattern).compile()
    except ErreurConfig as e:
        print(e, file=sys.stderr)
        return 2
    if not r.rx.search(args.phrase.lower()) and not r.rx.search(args.phrase):
        print("Le motif ne reconnaît pas la phrase d'origine. Passez --pattern.", file=sys.stderr)
        return 2
    print(f"Motif : {pattern}\n")
    ref = corpus.files([args.corpus] if args.corpus else [corpus.default_dir()])
    if ref:
        m = apprendre.mesure(pattern, ref)
        print(f"Corpus humain : {m['hits']} occurrence(s) sur {m['mots']} mots ({m['taux']:.3f} pour 1 000)")
        for e in m["exemples"]:
            print("   ", e)
        sev = apprendre.verdict(m["taux"], m["hits"])
    else:
        print("Pas de corpus humain : lancez « slopcheck corpus fetch » pour mesurer les faux positifs.")
        sev = "warn"
    if args.files:
        m2 = apprendre.mesure(pattern, corpus.files(args.files))
        print(f"\nVos fichiers : {m2['hits']} occurrence(s) sur {m2['mots']} mots")
        for e in m2["exemples"]:
            print("   ", e)
    if sev == "trop-large":
        print("\nVerdict : motif trop large, il touche la prose humaine. Resserrez-le avec --pattern.")
        if args.save and not args.force:
            return 1
        sev = "warn"
    else:
        print(f"\nSévérité conseillée : {sev.upper()}")
    if args.severity:
        sev = args.severity
    if args.save:
        rid = args.id or apprendre.slug(args.phrase)
        bloc = apprendre.bloc_toml(rid, pattern, sev, args.message or f"Tournure rejetée : « {args.phrase} ».",
                                   args.fix or "Écrire le fait à la place.", args.phrase)
        apprendre.sauve(Path(args.save), bloc)
        print(f"Règle « {rid} » ajoutée à {args.save}. Chargez ce pack dans .slopcheck.toml (packs = [..., \"{args.save}\"]).")
    return 0


def cmd_corpus(args) -> int:
    if args.action == "path":
        print(corpus.default_dir())
        return 0
    dest = corpus.fetch(Path(args.dest) if args.dest else None)
    print(f"\nCorpus dans {dest}")
    return 0


def cmd_init(args) -> int:
    p = Path(".slopcheck.toml")
    if p.exists() and not args.force:
        print(".slopcheck.toml existe déjà (--force pour écraser).", file=sys.stderr)
        return 1
    p.write_text(INIT, encoding="utf-8")
    print(f"Configuration écrite : {p.resolve()}")
    return 0


def parser():
    ap = argparse.ArgumentParser(prog="slopcheck", description="Détecteur des tics d'écriture IA en français.")
    ap.add_argument("--version", action="version", version=f"slopcheck {__version__}")
    sp = ap.add_subparsers(dest="cmd")

    p = sp.add_parser("check", help="analyser des fichiers (commande par défaut)")
    p.add_argument("files", nargs="+", help="fichiers, ou - pour l'entrée standard")
    p.add_argument("--format", choices=["text", "json", "github"], default="text")
    p.add_argument("--summary", action="store_true", help="comptage par règle au lieu du détail")
    p.add_argument("--min-severity", choices=["warn", "block"], default="warn")
    _ajoute_options_regles(p)
    p.set_defaults(fn=cmd_check)

    p = sp.add_parser("rules", help="lister les règles chargées")
    p.add_argument("code", nargs="?", help="détail d'une règle")
    _ajoute_options_regles(p)
    p.set_defaults(fn=cmd_rules)

    p = sp.add_parser("test", help="vérifier les exemples de chaque règle")
    p.add_argument("--config")
    p.add_argument("--pack", action="append")
    p.set_defaults(fn=cmd_test)

    p = sp.add_parser("bench", help="taux d'alertes pour 1 000 mots sur un corpus")
    p.add_argument("paths", nargs="*", help="fichiers ou dossiers (défaut : corpus de référence)")
    p.add_argument("--chunk", type=int, default=1500, help="découpe en morceaux de N mots (0 : aucun)")
    p.add_argument("--top", type=int, default=30)
    p.add_argument("--by-file", action="store_true")
    _ajoute_options_regles(p)
    p.set_defaults(fn=cmd_bench)

    p = sp.add_parser("learn", help="transformer une phrase rejetée en règle")
    p.add_argument("phrase")
    p.add_argument("files", nargs="*", help="vos textes, pour voir où le motif apparaît")
    p.add_argument("--pattern", help="motif regex à la place du motif généré")
    p.add_argument("--exact", action="store_true", help="ne pas assouplir les déterminants")
    p.add_argument("--corpus", help="corpus humain (défaut : corpus de référence téléchargé)")
    p.add_argument("--save", help="pack .toml où écrire la règle")
    p.add_argument("--id")
    p.add_argument("--severity", choices=["block", "warn"])
    p.add_argument("--message")
    p.add_argument("--fix")
    p.add_argument("--force", action="store_true", help="enregistrer même un motif trop large")
    p.set_defaults(fn=cmd_learn)

    p = sp.add_parser("corpus", help="télécharger le corpus humain de référence")
    p.add_argument("action", choices=["fetch", "path"])
    p.add_argument("--dest")
    p.set_defaults(fn=cmd_corpus)

    p = sp.add_parser("init", help="créer un .slopcheck.toml dans le dossier courant")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_init)
    return ap


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in SOUS_COMMANDES and argv[0] not in ("-h", "--help", "--version"):
        argv.insert(0, "check")
    args = parser().parse_args(argv)
    if not getattr(args, "fn", None):
        parser().print_help()
        return 2
    try:
        return args.fn(args)
    except ErreurConfig as e:
        print(f"slopcheck : {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
