"""Vérifications intégrées. Chaque fonction reçoit (règle, document) et
produit des Hit. Les listes de mots passent par `rule.params` : un pack peut
les compléter avec `params_add` sans toucher au code."""
import re
from collections import defaultdict
from dataclasses import dataclass



@dataclass
class Hit:
    rule: object
    line: int
    excerpt: str
    severity: str = ""
    note: str = ""


def _blocks(rule, doc):
    for b in doc.blocks:
        if b.kind in rule.kinds:
            yield b


def _units(rule, b):
    if rule.scope in ("block", "title"):
        return [(0, b.text)]
    ph = b.sentences()
    if rule.scope == "sentence":
        return ph
    if rule.scope == "first_sentence":
        return ph[:1]
    if rule.scope == "last_sentence":
        return ph[-1:] if len(ph) >= rule.min_sentences else []
    return []


def _court(s, n=70):
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def check_regex(rule, doc):
    if rule.scope == "raw":
        for n, line in enumerate(doc.raw_lines, 1):
            if n in doc.off_lines:
                continue
            m = rule.rx.search(line)
            if m and not (rule.rx_unless and rule.rx_unless.search(line)):
                yield Hit(rule, n, _court(m.group(0)))
        return
    for b in _blocks(rule, doc):
        if rule.scope == "title" and not b.is_title:
            continue
        n = 0
        for start, txt in _units(rule, b):
            if rule.rx_unless and rule.rx_unless.search(txt):
                continue
            for m in rule.rx.finditer(txt):
                yield Hit(rule, b.line_at(start + m.start()), _court(m.group(0)))
                n += 1
                if n >= rule.max_per_block:
                    break
            if n >= rule.max_per_block:
                break


RE_INTERRO = re.compile(r"\b(?:qu['’]est-ce|est-ce)\s+qu(?:e\b|['’])|\bqu['’]est-ce qui\b", re.I)
RE_RELATIF = re.compile(r"\b([\wÀ-ÿ]+)\s+(?:qui|que|dont|où)\s+[\wÀ-ÿ]+|\b([\wÀ-ÿ]+)\s+qu['’][\wÀ-ÿ]+", re.I)
# Mots après lesquels « que » est une conjonction ou un comparatif, pas un relatif.
AVANT_CONJONCTION = set("""plutôt avant après alors dès pour bien ainsi tant sans afin parce pendant tandis depuis
jusqu moins plus autre autres même si aussi tel telle tels telles faut sait dit pense crois est sont était ne
vérifier savoir dire penser croire montrer prouver comprendre sachant sorte façon manière lorsque puisque quoique
que qu""".split())


def check_title_relative(rule, doc):
    """Titre ou étiquette en proposition relative : « Le seuil qui déclenche »."""
    for b in _blocks(rule, doc):
        if not b.is_title:
            continue
        t = RE_INTERRO.sub(" ", b.text)
        for m in RE_RELATIF.finditer(t):
            avant = (m.group(1) or m.group(2)).lower()
            if avant in AVANT_CONJONCTION or re.search(r"(?:er|ir|oir|re)$", avant) and m.group(2):
                continue
            yield Hit(rule, b.line, _court(m.group(0)))
            break


def check_passive(rule, doc):
    p = rule.params
    etre = r"(?:est|sont|était|étaient|sera|seront|serait|seraient|a été|ont été|avait été|avaient été|soit|soient|fut|furent|être|été)"
    irr = "|".join(p.get("participes_irreguliers", []))
    rx = re.compile(
        rf"\b{etre}\s+(?:\w+ment\s+|bien\s+|déjà\s+|encore\s+|toujours\s+|souvent\s+)?"
        rf"(?P<part>{irr + '|' if irr else ''}\w{{3,}}(?:é|ée|és|ées))\b", re.I)
    actifs = set(p.get("participes_actifs", []))
    for b in _blocks(rule, doc):
        for m in rx.finditer(b.text):
            if m.group("part").lower() in actifs:
                continue
            if re.search(r"\b(?:s['’]|se |me |te |nous |vous |m['’]|t['’])\w*\s*$", b.text[: m.start()], re.I):
                continue
            yield Hit(rule, b.line_at(m.start()), _court(m.group(0)))


def check_participe_final(rule, doc):
    gerondifs = set(rule.params.get("gerondifs", []))
    rx = re.compile(r",\s+([a-zà-ÿ]{4,}ant)\s+[^.!?]{4,}[.!?]?\s*$", re.I)
    for b in _blocks(rule, doc):
        for start, ph in b.sentences():
            m = rx.search(ph)
            if m and m.group(1).lower() in gerondifs:
                yield Hit(rule, b.line_at(start + m.start()), _court(m.group(0), 60))
                break


def check_hedges(rule, doc):
    rxs = [re.compile(rf"\b{h}\b", re.I) for h in rule.params.get("hedges", [])]
    seuil = rule.params.get("min", 2)
    for b in _blocks(rule, doc):
        for start, ph in b.sentences():
            trouves = [r.search(ph).group(0) for r in rxs if r.search(ph)]
            if len(trouves) >= seuil:
                yield Hit(rule, b.line_at(start), ", ".join(trouves[:3]))
                break


def check_staccato(rule, doc):
    maxi = rule.params.get("max_words", 4)
    suite = rule.params.get("run", 3)
    for b in _blocks(rule, doc):
        if b.kind == "heading":
            continue
        run = []
        for start, ph in b.sentences():
            if 1 <= len(ph.split()) <= maxi:
                run.append((start, ph))
                if len(run) >= suite:
                    yield Hit(rule, b.line_at(run[0][0]), _court(" ".join(p for _, p in run), 60))
                    break
            else:
                run = []


def check_anaphore(rule, doc):
    maxi_court = rule.params.get("short_words", 5)
    suite = []
    for b in doc.blocks:
        if b.kind != "paragraph":
            suite = []
            continue
        for start, ph in b.sentences():
            m = re.match(r"[«\"'\s]*([A-Za-zÀ-ÿ']{2,})", ph)
            if not m:
                suite = []
                continue
            suite.append((b.line_at(start), m.group(1).lower(), ph))
            if len(suite) >= 3:
                trois = suite[-3:]
                if len({x[1] for x in trois}) == 1 and trois[-1][0] - trois[0][0] <= 3:
                    courtes = all(len(x[2].split()) <= maxi_court for x in trois)
                    yield Hit(rule, trois[0][0], f"« {trois[0][1]} » x3",
                              severity="" if courtes else "warn")
                    suite = []


def check_repetition(rule, doc):
    """Un terme répété : alerte à la n-ième occurrence (métaphores usées, mots passe-partout)."""
    termes = rule.params.get("terms", [])
    mini = rule.params.get("min", 2)
    pos = defaultdict(list)
    for b in _blocks(rule, doc):
        for t in termes:
            for m in re.finditer(rf"\b{t}\b", b.text, re.I):
                pos[t].append(b.line_at(m.start()))
    for t, lignes in pos.items():
        if len(lignes) >= mini:
            nom = re.sub(r"[\\()?:|\[\]]", "", t)
            yield Hit(rule, lignes[mini - 1], f"« {nom} » x{len(lignes)} (lignes {', '.join(map(str, lignes[:5]))})")


def check_lexical_density(rule, doc):
    """Vocabulaire par défaut des modèles : seul, un mot passe ; plusieurs
    distincts dans le même paragraphe trahissent le réflexe."""
    termes = [(t, re.compile(rf"\b{t}\b", re.I)) for t in rule.params.get("terms", [])]
    mini = rule.params.get("min_distinct", 3)
    for b in _blocks(rule, doc):
        trouves = []
        for t, rx in termes:
            m = rx.search(b.text)
            if m:
                trouves.append(m)
        trouves.sort(key=lambda m: (m.start(), -m.end()))
        gardes = []
        for m in trouves:
            if not gardes or m.start() >= gardes[-1].end():
                gardes.append(m)
        trouves = gardes
        if len(trouves) >= mini:
            yield Hit(rule, b.line_at(trouves[0].start()), ", ".join(m.group(0) for m in trouves[:5]))


def check_objet_agent(rule, doc):
    humains = {h.lower() for h in rule.params.get("sujets_humains", [])}
    verbes = "|".join(rule.params.get("verbes", []))
    rx = re.compile(
        r"\b(?:(?:le|la|les|ce|cet|cette|ces|votre|vos|notre|nos|son|sa|ses|leur|leurs|ton|ta|tes)\s+|l['’])"
        rf"(?P<nom>[a-zàâçéèêëîïôûùüÿœ][\w'-]+)\s+(?:(?:ne|n['’])\s?)?(?:{verbes})\b", re.I)
    for b in _blocks(rule, doc):
        for m in rx.finditer(b.text):
            nom = m.group("nom")
            if nom[0].isupper():
                continue
            base = nom.lower()
            if base in humains or base.rstrip("sx") in humains or base[:-1] in humains:
                continue
            if base.startswith(("qu'", "qu’")):
                continue
            suite = b.text[m.end():m.end() + 16].lower()
            if suite.startswith(" dire") and "veu" in m.group(0).lower():
                continue
            if "parl" in m.group(0).lower() and re.match(r"\s+(?:de |d['’]|des |du )(?!eux-mêmes|lui-même|elle-même)", suite):
                continue
            yield Hit(rule, b.line_at(m.start()), _court(m.group(0), 60))


def check_question_reponse(rule, doc):
    maxi = rule.params.get("max_words", 4)
    rx = re.compile(r"[^.!?]{4,90}\?\s+([A-ZÀ-Ý][^.!?]{0,45}[.!])")
    for b in _blocks(rule, doc):
        if b.dialogue or b.kind == "heading":
            continue
        for m in rx.finditer(b.text):
            if len(m.group(1).split()) <= maxi:
                yield Hit(rule, b.line_at(m.start()), _court(m.group(0)[-60:]))
                break


RE_EMOJI = "[\U0001F300-\U0001FAFF\u2600-\u2604\u2607-\u27BF\u2B50\u2B55]\uFE0F?"
# « **Mot** : », « **Mot :** », avec ou sans émoji devant.
RE_PUCE_GRAS = re.compile(rf"^\s*(?:{RE_EMOJI}\s*)?\*\*[^*]{{2,80}}?(?:\*\*\s*[:.\u2013\u2014-]|\s*[:.]\s*\*\*)")
RE_EMOJI_TETE = re.compile(rf"^\s*(?:\*\*)?{RE_EMOJI}\s*(?:\*\*)?\S")


def check_emoji_lead(rule, doc):
    """Émoji en tête de ligne, de puce ou d'intertitre. Un seul se relit ;
    à partir de `block_at` lignes, c'est la mise en page d'un générateur."""
    block_at = rule.params.get("block_at", 2)
    signaletique = tuple(rule.params.get("signaletique", ["⚠", "ℹ", "❗"]))
    lignes, decor = [], 0
    for b in _blocks(rule, doc):
        for off, num in zip(b.offsets, b.lines):
            debut = b.text[off:off + 12]
            if RE_EMOJI_TETE.match(debut):
                lignes.append((num, _court(b.text[off:], 50)))
                decor += not debut.lstrip(" *").startswith(signaletique)
    sev = "block" if decor >= block_at else "warn"
    for num, ex in lignes[:3]:
        yield Hit(rule, num, ex, severity=sev,
                  note=f"x{len(lignes)} lignes ouvertes par un émoji" if len(lignes) > 1 else "")


def check_bold_bullets(rule, doc):
    warn_at = rule.params.get("warn_at", 4)
    block_at = rule.params.get("block_at", 7)
    serie = []

    def flush():
        if len(serie) >= warn_at:
            yield Hit(rule, serie[0], f"x{len(serie)} puces « **Mot** : » d'affilée",
                      severity="block" if len(serie) >= block_at else "warn")

    for b in doc.blocks:
        if b.kind == "list" and RE_PUCE_GRAS.match(b.text):
            serie.append(b.line)
        else:
            yield from flush()
            serie = []
    yield from flush()


RE_FAQ = re.compile(r"\b(?:FAQ|questions? fréquentes?|foire aux questions|vos questions)\b", re.I)


def check_heading_questions(rule, doc):
    """Intertitres en question. Une section FAQ et ses sous-titres restent permis."""
    mini = rule.params.get("min", 3)
    q, faq = [], 0
    for b in doc.blocks:
        if b.kind != "heading":
            continue
        if faq and b.level <= faq:
            faq = 0
        if RE_FAQ.search(b.text):
            faq = b.level
            continue
        if not faq and b.text.rstrip().endswith("?"):
            q.append(b)
    if len(q) >= mini:
        yield Hit(rule, q[mini - 1].line, f"{len(q)} intertitres en question")


def check_title_case(rule, doc):
    petits = set(rule.params.get("mots_outils", []))
    for b in _blocks(rule, doc):
        if b.kind != "heading":
            continue
        mots = [m for m in re.findall(r"[A-Za-zÀ-ÿ'’-]+", b.text)][1:]
        pleins = [m for m in mots if len(m) >= 4 and m.lower() not in petits and not m.isupper()]
        if len(pleins) >= 3 and all(m[0].isupper() for m in pleins):
            yield Hit(rule, b.line, _court(b.text, 60))


RE_TIRET = re.compile(r"(?<![.!?…»]\s)(?<![.!?…»])(?:—|(?<=[^\d\s]\s)–(?=\s[^\d\s]))")


def check_em_dash(rule, doc):
    """Tiret cadratin en incise. Le tiret de dialogue en tête de réplique reste permis."""
    for b in _blocks(rule, doc):
        if b.dialogue:
            continue
        found = list(RE_TIRET.finditer(b.text))
        if found:
            m = found[0]
            yield Hit(rule, b.line_at(m.start()), _court(b.text[max(0, m.start() - 25): m.end() + 25], 60))


def check_h1_duplicate(rule, doc):
    if not doc.frontmatter.get("title"):
        return
    for b in doc.blocks:
        if b.kind == "heading" and doc.raw_lines[b.line - 1].lstrip().startswith("# "):
            yield Hit(rule, b.line, _court(b.text, 50))
            return


def check_ghost_table(rule, doc):
    rx = re.compile(rule.params.get("heading", r"tableau (?:comparatif|récapitulatif)"), re.I)
    for i, b in enumerate(doc.blocks):
        if b.kind == "heading" and rx.search(b.text):
            suite = doc.blocks[i + 1: i + 12]
            fin = next((j for j, x in enumerate(suite) if x.kind == "heading"), len(suite))
            if not any(x.kind == "table" for x in suite[:fin]):
                yield Hit(rule, b.line, _court(b.text, 50))


CHECKS = {
    "regex": check_regex,
    "title_relative": check_title_relative,
    "passive": check_passive,
    "participe_final": check_participe_final,
    "hedges": check_hedges,
    "staccato": check_staccato,
    "anaphore": check_anaphore,
    "repetition": check_repetition,
    "lexical_density": check_lexical_density,
    "objet_agent": check_objet_agent,
    "question_reponse": check_question_reponse,
    "bold_bullets": check_bold_bullets,
    "emoji_lead": check_emoji_lead,
    "heading_questions": check_heading_questions,
    "title_case": check_title_case,
    "em_dash": check_em_dash,
    "h1_duplicate": check_h1_duplicate,
    "ghost_table": check_ghost_table,
}
