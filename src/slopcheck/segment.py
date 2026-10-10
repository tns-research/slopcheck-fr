"""Découpage d'un texte (markdown ou brut) en blocs de prose.

Un paragraphe coupé à 70 caractères est recollé avant analyse : les règles
voient des paragraphes, jamais des lignes physiques. Chaque bloc garde la
correspondance position -> ligne source pour les rapports.
"""
import re
from bisect import bisect_right
from dataclasses import dataclass, field

RE_FENCE = re.compile(r"^\s*(```|~~~)")
RE_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
RE_LIST = re.compile(r"^(\s*)(?:[-*+]|\d{1,3}[.)])\s+")
RE_QUOTE = re.compile(r"^\s*>\s?")
RE_TABLE = re.compile(r"^\s*\|")
RE_HR = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")
RE_SETEXT = re.compile(r"^\s*=+\s*$")
RE_HTML_OPEN = re.compile(r"^\s*<(script|style)\b", re.I)
RE_HTML_CLOSE = re.compile(r"</(?:script|style)>", re.I)
RE_DIRECTIVE = re.compile(r"<!--\s*slopcheck\s*:\s*(ignore|off|on|disable)\b(.*?)-->", re.I)
RE_COMMENT_LINE = re.compile(r"^\s*<!--.*-->\s*$")
RE_SENT_END = re.compile(r"(?<=[.!?…])[»\"”)\]*_]*\s+")
RE_WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿœŒ0-9]+(?:['’-][A-Za-zÀ-ÖØ-öø-ÿœŒ0-9]+)*")

PROSE_KINDS = ("paragraph", "list", "quote", "heading")
PRONOMS_SUJETS = {"je", "j'ai", "il", "elle", "on", "nous", "vous", "ils", "elles", "tu"}


def _blank(m):
    return " " * len(m.group(0))


def _link(m):
    texte = m.group(1)
    return " " + texte + " " * (len(m.group(0)) - len(texte) - 1)


def mask(text: str) -> str:
    """Efface code en ligne, URL, cibles de liens et balises, à longueur égale."""
    text = re.sub(r"`[^`\n]*`", _blank, text)
    text = re.sub(r"!\[[^\]\n]*\]\([^)\n]*\)", _blank, text)
    text = re.sub(r"\[([^\]\n]*)\]\([^)\n]*\)", _link, text)
    text = re.sub(r"<!--.*?-->", _blank, text)
    text = re.sub(r"</?[A-Za-z][^>\n]*>", _blank, text)
    text = re.sub(r"https?://\S+", _blank, text)
    return text


def est_titre(l: str) -> bool:
    """Titre, ligne en gras seule, ou étiquette courte."""
    l = l.strip()
    if not l or l.startswith(("«", "“", '"', "|")):
        return False
    if re.fullmatch(r"\*\*[^*]+\*\*:?", l):
        return True
    if l.endswith(":"):
        mots = l.split()
        return len(mots) <= 9 and mots[0].lower() not in PRONOMS_SUJETS
    if l.split()[0].lower() in PRONOMS_SUJETS:
        return False
    return len(l) <= 70 and not l.endswith((".", "!", "?", ":", ";", ",", "…", "»", ")"))


@dataclass
class Block:
    kind: str
    text: str = ""
    offsets: list = field(default_factory=list)
    lines: list = field(default_factory=list)
    is_title: bool = False
    dialogue: bool = False
    level: int = 0

    @property
    def line(self) -> int:
        return self.lines[0]

    def add(self, content: str, lineno: int):
        if self.text:
            self.text += " "
        self.offsets.append(len(self.text))
        self.lines.append(lineno)
        self.text += content

    def line_at(self, pos: int) -> int:
        i = bisect_right(self.offsets, pos) - 1
        return self.lines[max(i, 0)]

    def sentences(self):
        """[(position de début, phrase)]"""
        out, start = [], 0
        for m in RE_SENT_END.finditer(self.text):
            seg = self.text[start:m.start()].strip()
            if seg:
                out.append((start, self.text[start:m.start()]))
            start = m.end()
        if self.text[start:].strip():
            out.append((start, self.text[start:]))
        return out


@dataclass
class Document:
    name: str
    raw_lines: list
    blocks: list
    ignored: dict
    disabled: set
    off_lines: set
    frontmatter: dict

    @property
    def words(self) -> int:
        return sum(len(RE_WORD.findall(b.text)) for b in self.blocks if b.kind in PROSE_KINDS)


def _frontmatter(lines):
    if not lines or lines[0].strip() not in ("---", "+++"):
        return 0, {}
    fin = lines[0].strip()
    for j in range(1, len(lines)):
        if lines[j].strip() == fin:
            data = {}
            for l in lines[1:j]:
                m = re.match(r"^([A-Za-z_][\w-]*)\s*[:=]\s*(.*)$", l)
                if m:
                    data[m.group(1)] = m.group(2).strip().strip("\"'")
            return j + 1, data
    return 0, {}


def parse(name: str, text: str) -> Document:
    lines = text.splitlines()
    debut, fm = _frontmatter(lines)
    blocks, ignored, disabled, off_lines = [], {}, set(), set(range(1, debut + 1))
    cur = None
    in_fence = in_html = in_comment = off = False
    pending = None

    def flush():
        nonlocal cur, pending
        if cur is None:
            return
        brut = cur.text
        cur.text = mask(brut)
        if cur.kind == "heading":
            cur.is_title = True
        elif cur.kind in ("paragraph", "list") and len(cur.lines) == 1:
            cur.is_title = est_titre(brut)
        cur.dialogue = cur.text.lstrip().startswith(("—", "–"))
        if pending:
            for n in cur.lines:
                ignored.setdefault(n, set()).update(pending)
            pending = None
        if cur.text.strip():
            blocks.append(cur)
        cur = None

    for idx in range(debut, len(lines)):
        n, line = idx + 1, lines[idx]
        for m in RE_DIRECTIVE.finditer(line):
            verbe = m.group(1).lower()
            codes = set(re.findall(r"[\w-]+", m.group(2))) or {"*"}
            if verbe == "ignore":
                if RE_DIRECTIVE.sub("", line).strip():
                    ignored.setdefault(n, set()).update(codes)
                else:
                    pending = codes
            elif verbe == "off":
                off = True
            elif verbe == "on":
                off = False
            elif verbe == "disable":
                disabled |= codes
        if off:
            off_lines.add(n)
            flush()
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if RE_FENCE.match(line):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if in_html:
            if RE_HTML_CLOSE.search(line):
                in_html = False
            continue
        if RE_HTML_OPEN.match(line):
            flush()
            in_html = not RE_HTML_CLOSE.search(line)
            continue
        if RE_COMMENT_LINE.match(line):
            continue
        if line.lstrip().startswith("<!--"):
            in_comment = "-->" not in line
            continue
        if not line.strip():
            flush()
            continue
        if RE_HR.match(line):
            flush()
            continue
        if RE_SETEXT.match(line) and cur is not None and cur.kind == "paragraph" and len(cur.lines) == 1:
            cur.kind = "heading"
            cur.level = 1
            flush()
            continue
        m = RE_HEADING.match(line)
        if m:
            flush()
            cur = Block("heading", level=len(m.group(1)))
            cur.add(m.group(2), n)
            flush()
            continue
        if RE_TABLE.match(line):
            flush()
            cur = Block("table")
            cur.add(line.strip(), n)
            flush()
            continue
        m = RE_LIST.match(line)
        if m:
            flush()
            cur = Block("list")
            cur.add(line[m.end():].strip(), n)
            continue
        m = RE_QUOTE.match(line)
        if m:
            if cur is None or cur.kind != "quote":
                flush()
                cur = Block("quote")
            cur.add(line[m.end():].strip(), n)
            continue
        if cur is None:
            cur = Block("paragraph")
        cur.add(line.strip(), n)
    flush()
    return Document(name, lines, blocks, ignored, disabled, off_lines, fm)
