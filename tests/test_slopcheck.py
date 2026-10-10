import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from slopcheck import regles
from slopcheck.apprendre import motif
from slopcheck.cli import main
from slopcheck.moteur import analyse, decoupe
from slopcheck.segment import parse


def codes(texte, packs=("fr-signatures", "typo-fr")):
    rs = regles.RuleSet()
    for p in packs:
        rs.load_file(regles.resolve_pack(p, Path.cwd()))
    return {c.code for c in analyse("t", texte, rs.rules())[0]}


def run(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = main(list(argv))
    return rc, buf.getvalue()


class Segmentation(unittest.TestCase):
    def test_paragraphe_coupe_recolle(self):
        doc = parse("t", "Il marchait le long\nde la rivière qui\ncoulait vers le sud.\n")
        self.assertEqual(len(doc.blocks), 1)
        self.assertFalse(doc.blocks[0].is_title)
        self.assertEqual(doc.blocks[0].text, "Il marchait le long de la rivière qui coulait vers le sud.")

    def test_ligne_source(self):
        doc = parse("t", "Premier.\n\nUn deux\ntrois quatre — cinq.\n")
        b = doc.blocks[1]
        self.assertEqual(b.line_at(b.text.index("—")), 4)

    def test_code_frontmatter_html(self):
        texte = "---\ntitle: X\n---\n\n```\nCe n'est pas X, c'est Y.\n```\n\n<script>\nvar a = 'qui change tout';\n</script>\n\nTexte.\n"
        doc = parse("t", texte)
        self.assertEqual([b.text for b in doc.blocks], ["Texte."])
        self.assertEqual(doc.frontmatter["title"], "X")

    def test_titres_et_listes(self):
        doc = parse("t", "# Titre\n\n- un élément\n  qui continue\n- deux\n\n> cité\n> encore\n")
        self.assertEqual([b.kind for b in doc.blocks], ["heading", "list", "list", "quote"])
        self.assertEqual(doc.blocks[1].text, "un élément qui continue")

    def test_code_en_ligne_et_url_masques(self):
        self.assertNotIn("qui-change-tout", codes("Voir `ce qui change tout` et https://x.fr/qui-change-tout ici."))

    def test_dialogue(self):
        self.assertNotIn("em-dash", codes("— Bonjour, dit-il.\n\nIl se tut. — Et vous ? demanda-t-elle.\n"))
        self.assertIn("em-dash", codes("Le produit — lancé en mars — a trouvé son public.\n"))

    def test_etiquette_phrase_longue(self):
        doc = parse("t", "Il écrivit sous la dictée de Fantine cette lettre qu'il lui fit signer:\n")
        self.assertFalse(doc.blocks[0].is_title)


class Suppression(unittest.TestCase):
    def test_ignore_bloc_suivant(self):
        t = "<!-- slopcheck: ignore -->\nCe n'est pas un outil, c'est un partenaire.\n"
        self.assertNotIn("correction-deux-temps", codes(t))

    def test_ignore_code_precis(self):
        t = "<!-- slopcheck: ignore em-dash -->\nCe n'est pas un outil, c'est un partenaire — vraiment.\n"
        c = codes(t)
        self.assertIn("correction-deux-temps", c)
        self.assertNotIn("em-dash", c)

    def test_off_on(self):
        t = "<!-- slopcheck: off -->\nEt voici pourquoi.\n<!-- slopcheck: on -->\n\nEt voici pourquoi.\n"
        rs = regles.load(no_config=True)
        constats = analyse("t", t, rs.rules())[0]
        self.assertEqual([c.line for c in constats if c.code == "fausse-revelation"], [5])

    def test_disable_fichier(self):
        self.assertNotIn("fausse-revelation", codes("<!-- slopcheck: disable mise-en-scene -->\n\nEt voici pourquoi.\n"))


class Config(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_pack_perso_et_surcharges(self):
        (self.d / "perso.toml").write_text(
            "[pack]\nname = \"perso\"\n\n[[rule]]\nid = \"au-final\"\nseverity = \"block\"\n"
            "pattern = '''\\bau final\\b'''\nmessage = \"m\"\nfix = \"f\"\nbad = [\"Au final, oui.\"]\n",
            encoding="utf-8")
        (self.d / ".slopcheck.toml").write_text(
            "packs = [\"fr-strict\", \"./perso.toml\"]\ndisable = [\"voix-passive\"]\n\n"
            "[severity]\nem-dash = \"warn\"\n\n[params_add.objet-agent]\nsujets_humains = [\"chapeau\"]\n",
            encoding="utf-8")
        rs = regles.load(str(self.d / ".slopcheck.toml"))
        rules = {r.id: r for r in rs.rules()}
        self.assertIn("au-final", rules)
        self.assertNotIn("voix-passive", rules)
        self.assertEqual(rules["em-dash"].severity, "warn")
        self.assertIn("chapeau", rules["objet-agent"].params["sujets_humains"])
        texte = "Au final, le chapeau décide du reste.\n"
        trouves = {c.code for c in analyse("t", texte, rs.rules())[0]}
        self.assertIn("au-final", trouves)
        self.assertNotIn("objet-agent", trouves)

    def test_erreurs_lisibles(self):
        (self.d / "c.toml").write_text("packs = [\"inexistant\"]\n", encoding="utf-8")
        with self.assertRaises(regles.ErreurConfig):
            regles.load(str(self.d / "c.toml"))
        (self.d / "c.toml").write_text("[[rule]]\nid = \"x\"\npattern = '''(('''\n", encoding="utf-8")
        with self.assertRaises(regles.ErreurConfig):
            regles.load(str(self.d / "c.toml")).rules()

    def test_strict_etend_signatures(self):
        rs = regles.load(no_config=True, packs=["fr-strict"])
        rules = {r.id: r for r in rs.rules()}
        self.assertEqual(rules["em-dash"].severity, "block")
        self.assertIn("ouverture-cliche", rules)


class Moteur(unittest.TestCase):
    def test_escalade(self):
        t = "C'est un véritable atout.\n\nUne véritable révolution.\n"
        rs = regles.load(no_config=True)
        sev = [c.severity for c in analyse("t", t, rs.rules())[0] if c.code == "veritable"]
        self.assertEqual(sev, ["block", "block"])

    def test_max_par_document(self):
        t = "\n\n".join("Vous venez jeudi?" for _ in range(6))
        rs = regles.load(no_config=True)
        c = [x for x in analyse("t", t, rs.rules())[0] if x.code == "espace-ponctuation"]
        self.assertEqual(len(c), 3)
        self.assertIn("non affichée", c[-1].note)

    def test_decoupe(self):
        t = "\n\n".join("mot " * 100 for _ in range(10))
        self.assertEqual(len(list(decoupe(t, 300))), 4)

    def test_motif_learn(self):
        import re
        m = motif("Au final, c'est le client qui décide")
        self.assertTrue(re.search(m, "au final, c’est votre client qui décide", re.I))


class Cli(unittest.TestCase):
    def test_codes_retour_et_json(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write("Dans un monde en constante évolution, tout change.\n")
        try:
            rc, out = run("--no-config", "--format", "json", f.name)
            self.assertEqual(rc, 1)
            self.assertEqual(json.loads(out)["findings"][0]["code"], "ouverture-cliche")
            Path(f.name).write_text("Le 4 mars, Marc a signé son premier client.\n", encoding="utf-8")
            rc, _ = run("--no-config", f.name)
            self.assertEqual(rc, 0)
        finally:
            os.unlink(f.name)

    def test_exemples_des_packs(self):
        rc, out = run("test")
        self.assertEqual(rc, 0, out)


def constats(texte, packs=("fr-signatures", "typo-fr")):
    rs = regles.RuleSet()
    for p in packs:
        rs.load_file(regles.resolve_pack(p, Path.cwd()))
    return analyse("t", texte, rs.rules())[0]


class DixTics(unittest.TestCase):
    def test_emoji_tete_signaletique_reste_warn(self):
        c = [x for x in constats("### ⚠️ Version obsolète\n\n### ⚠️ Ne pas utiliser\n") if x.code == "emoji-tete"]
        self.assertTrue(c)
        self.assertTrue(all(x.severity == "warn" for x in c))
        c = [x for x in constats("🚀 On recrute.\n\n💡 Télétravail.\n") if x.code == "emoji-tete"]
        self.assertTrue(all(x.severity == "block" for x in c))

    def test_puces_gras_deux_points_dedans(self):
        t = "- **Vitesse :** rapide.\n- **Prix :** bas.\n- **Support :** 24/7.\n"
        self.assertIn("puces-gras-serie", codes(t))

    def test_contraste_appose_article_relu(self):
        t = "Créez-la au nom de la société, et non au nom d'un associé.\n\nCandidatez quand vous commencez, pas trois mois avant.\n"
        c = [x for x in constats(t) if x.code == "contraste-appose"]
        self.assertEqual(len(c), 2)
        self.assertTrue(all(x.severity == "block" for x in c))

    def test_hashtags_et_titres_markdown(self):
        self.assertIn("hashtags", codes("Merci à tous. #Tech #Paris #Innovation\n"))
        self.assertNotIn("hashtags", codes("# Titre\n\n## Sous-titre\n\nVoir l'issue #42.\n"))


class SortieGithub(unittest.TestCase):
    def test_annotation_echappee(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "a,b:c.md"
            f.write_text("Ligne un — test\n", encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                main(["check", "--no-config", "--format", "github", str(f)])
        ligne = out.getvalue().strip()
        self.assertIn("a%2Cb%3Ac.md,line=1,", ligne)
        self.assertEqual(ligne.count("::"), 2)


if __name__ == "__main__":
    unittest.main()
