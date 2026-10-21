import json
import string
import tempfile
import unittest
from datetime import date
from pathlib import Path

import chunks
from chunks import study
from chunks.core import Phrase


class TestChunkAsFunction(unittest.TestCase):
    def test_returns_english_phrase(self):
        p = chunks.could_i_get("a glass of water")
        self.assertIsInstance(p, Phrase)
        self.assertEqual(p, "Could I get a glass of water, please?")

    def test_tuple_translates_variable(self):
        p = chunks.could_i_get(("a coffee", "um café"))
        self.assertEqual(p.en, "Could I get a coffee, please?")
        self.assertEqual(p.pt, "Pode me trazer um café, por favor?")

    def test_keyword_arguments(self):
        p = chunks.let_me_loop_in(topic="the deploy", person="Ana")
        self.assertEqual(p, "Let me loop in Ana to help us with the deploy.")

    def test_default_and_empty_variable_leave_no_stray_spaces(self):
        self.assertEqual(chunks.keep_me_in_the_loop(), "Please keep me in the loop.")

    def test_missing_variable_raises(self):
        with self.assertRaises(TypeError):
            chunks.let_me_loop_in("Ana")

    def test_cloze_hides_only_the_fixed_part(self):
        p = chunks.could_i_get("a glass of water")
        self.assertEqual(p.cloze, "{{c1::Could I get}} a glass of water{{c1::, please}}?")

    def test_adjacent_fixed_parts_merge_into_one_cloze(self):
        self.assertEqual(
            chunks.im_running_late("ten minutes").cloze,
            "{{c1::I'm running late, I'll be there in}} ten minutes.",
        )

    def test_braces_in_variable_are_kept(self):
        self.assertEqual(chunks.how_much_is("{x}"), "How much is {x}?")

    def test_blanks_hint_hides_only_the_fixed_part(self):
        self.assertEqual(chunks.could_i_get("a glass of water").blanks, "_____ _ ___ a glass of water, ______?")

    def test_demos_cover_every_example(self):
        self.assertEqual(
            [p.pt for p in chunks.dont_forget_your.demos()[:3]],
            ["Não esqueça a sua mochila!", "Não esqueça o seu casaco!", "Não esqueça as suas chaves!"],
        )

    def test_signature_is_introspectable(self):
        self.assertEqual(chunks.let_me_loop_in.pattern, "let_me_loop_in(person, topic)")


class TestLibrary(unittest.TestCase):
    def test_every_chunk_is_consistent(self):
        for c in chunks.registry().values():
            with self.subTest(chunk=c.name):
                pt_slots = {f for _, f, _, _ in string.Formatter().parse(c.pt) if f}
                self.assertEqual(pt_slots, set(c.slots), "tradução usa variáveis diferentes")
                self.assertIn("[[", c.template)
                for demo in c.demos():
                    self.assertNotIn("[[", demo.en)
                    self.assertIn("{{c1::", demo.cloze)

    def test_examples_are_many_and_translated(self):
        for c in chunks.registry().values():
            with self.subTest(chunk=c.name):
                if c.slots:
                    self.assertGreaterEqual(len(c.examples), 10, "dê pelo menos 10 exemplos")
                for ex in c.examples:
                    for slot, value in ex.items():
                        self.assertIsInstance(value, tuple)
                        self.assertEqual(len(value), 3, f"{slot!r}: ('inglês', 'português', 'alemão')")
                for p in c.demos():
                    for bad in ("o(a)", "(a) ", "seu/sua", "o/a "):
                        self.assertNotIn(bad, p.pt, "deixe o artigo dentro da tradução da variável")
                demos = c.demos()
                for lang in ("en", "pt", "de"):
                    texts = [getattr(p, lang) for p in demos]
                    self.assertEqual(len(set(texts)), len(texts), f"frases repetidas em {lang}")

    def test_every_chunk_has_german(self):
        for c in chunks.registry().values():
            with self.subTest(chunk=c.name):
                self.assertIn("[[", c.de)
                for p in c.demos():
                    self.assertTrue(p.de)
                    self.assertIn("{{c1::", p.de_cloze)
                    self.assertNotIn("[[", p.de)

    def test_ex_helper(self):
        from chunks.core import ex

        self.assertEqual(
            ex(("a", "b"), "x | y | z ;; 1 | 2 | 3"),
            [{"a": ("x", "y", "z"), "b": ("1", "2", "3")}],
        )
        with self.assertRaisesRegex(ValueError, "esperado 2"):
            ex(("a", "b"), "x | y | z")

    def test_invalid_example_is_rejected(self):
        from chunks.core import Chunk

        with self.assertRaisesRegex(ValueError, "exemplo 1"):
            Chunk("x", "[[Hi]] {name}.", "Oi {name}.", "mine", [{"nome": "Ana"}])

    def test_every_chunk_is_importable_by_name(self):
        for name in chunks.registry():
            self.assertIs(getattr(chunks, name), chunks.get(name))

    def test_search(self):
        names = [c.name for c in chunks.search("água")] + [c.name for c in chunks.search("bandwidth")]
        self.assertIn("dont_have_the_bandwidth", names)

    def test_article_helper(self):
        self.assertEqual(chunks.a("apple"), "an apple")
        self.assertEqual(chunks.a("hour"), "an hour")
        self.assertEqual(chunks.a("university"), "a university")
        self.assertEqual(chunks.a("car"), "a car")


class TestStudy(unittest.TestCase):
    def test_check_ignores_case_and_punctuation(self):
        p = chunks.could_i_get("a glass of water")
        self.assertTrue(study.check("could i get a glass of water please", p))
        self.assertFalse(study.check("I want a glass of water", p))

    def test_check_german_accepts_missing_umlauts(self):
        p = chunks.could_i_get(("a glass of water", "um copo de água", "ein Glas Wasser"))
        self.assertEqual(p.de, "Könnte ich bitte ein Glas Wasser haben?")
        self.assertTrue(study.check("Könnte ich bitte ein Glas Wasser haben", p, "de"))
        self.assertTrue(study.check("konnte ich bitte ein glas wasser haben?", p, "de"))
        self.assertFalse(study.check("Ich will Wasser", p, "de"))
        self.assertTrue(study.check("strasse", chunks.how_much_is(("x", "y", "Straße")), "de") is False)
        self.assertEqual(study.normalize("Straße"), "strasse")

    def test_parse_langs(self):
        self.assertEqual(study.parse_langs("en+de"), ["en", "de"])
        self.assertEqual(study.parse_langs("de"), ["de"])
        with self.assertRaisesRegex(ValueError, "Idioma inválido"):
            study.parse_langs("fr")

    def test_anki_export_german(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "cards.txt"
            n = study.anki_export(path, "survival", ["en", "de"])
            lines = path.read_text(encoding="utf-8").splitlines()[4:]
        self.assertEqual(n, len(lines))
        self.assertTrue(any(l.startswith("{{c1::Könnte ich bitte}}") for l in lines))
        self.assertTrue(any("chunks::de" in l for l in lines))

    def test_leitner_boxes(self):
        progress, today = {}, date(2026, 1, 1)
        study.record(progress, "time_to", True, today)
        self.assertEqual(progress["time_to"], {"box": 2, "due": "2026-01-03"})
        study.record(progress, "time_to", False, today)
        self.assertEqual(progress["time_to"]["box"], 1)

    def test_due_chunks_skips_future_reviews(self):
        progress = {"time_to": {"box": 3, "due": "2099-01-01"}}
        due = study.due_chunks(progress, "home", date(2026, 1, 1))
        self.assertNotIn("time_to", [c.name for c in due])
        self.assertIn("time_for", [c.name for c in due])

    def test_anki_export(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "cards.txt"
            n = study.anki_export(path, "survival")
            lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[2], "#notetype:Cloze")
        self.assertEqual(len(lines), n + 4)
        self.assertEqual(lines[4].count("\t"), 2)

    def test_web_data_is_up_to_date(self):
        folder = Path(__file__).resolve().parent.parent / "web" / "src" / "data"
        files = (
            ("chunks.json", study.to_json()),
            ("interviews.json", study.interviews_json()),
            ("interview_prompts.json", study.prompts_json()),
        )
        for name, expected in files:
            with self.subTest(file=name):
                self.assertEqual(
                    (folder / name).read_text(encoding="utf-8"),
                    expected,
                    "Rode `python -m chunks json` para atualizar o app web.",
                )


class TestInterviews(unittest.TestCase):
    def test_sessions_are_well_formed(self):
        from chunks import interviews

        for session in interviews.sessions().values():
            stages = {s.id for s in session.stages}
            self.assertEqual(stages, {q.stage for q in session.questions}, "etapa sem perguntas")
            for q in session.questions:
                with self.subTest(question=q.id):
                    self.assertTrue(q.en.strip() and q.goal.strip() and q.answer.strip())
                    plain = interviews.plain(q.answer)
                    self.assertNotIn("[[", plain)
                    self.assertNotIn("((", plain)
                    self.assertEqual(q.answer.count("[["), q.answer.count("]]"))
                    self.assertEqual(q.answer.count("(("), q.answer.count("))"))

    def test_plain_marks_what_to_fill(self):
        from chunks import interviews

        self.assertEqual(
            interviews.plain("[[I currently work as]] a Data Analyst ((at X))."),
            "I currently work as a Data Analyst [at X].",
        )


if __name__ == "__main__":
    unittest.main()


class TestJobGeneration(unittest.TestCase):
    JOB = "We are hiring a Data Engineer to build pipelines in Python and SQL. " * 3

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_generates_a_full_session(self):
        from chunks.interviews import from_dict, generate, prompts, to_dict
        from chunks.llm import Ollama
        from tests.fake_ollama import FakeOllama

        steps = []
        with FakeOllama() as fake:
            session = generate.generate_session(
                self.JOB, "", Ollama(host=fake.url, model="fake:latest"), per_stage=4, on_progress=steps.append
            )
        self.assertEqual(session.title, "Data Engineer")
        self.assertEqual(session.company, "Acme Corp")
        self.assertEqual([s.id for s in session.stages], [s.id for s in prompts.STAGES])
        # 4 por etapa, 2 no encerramento; a pergunta vazia foi descartada.
        self.assertEqual(len(session.questions), 4 * 5 + 2)
        self.assertEqual(len({q.id for q in session.questions}), len(session.questions))
        q = session.questions[0]
        self.assertEqual(q.tips, ("Dica 1", "Dica 2", "Dica 3"))
        self.assertIn("((number of years))", q.answer)
        self.assertEqual(len(steps), 1 + len(prompts.STAGES))

        # Sem perfil, o prompt manda usar ((placeholders)); as perguntas já feitas vão no prompt.
        chat = fake.requests[2]["messages"][1]["content"]
        self.assertIn(prompts.NO_PROFILE, chat)
        self.assertIn("Recrutador question 1?", chat)
        self.assertEqual(fake.requests[1]["format"], prompts.QUESTIONS_SCHEMA)

        # Salva e carrega de volta igual.
        path = generate.save(session, Path(self.tmp.name))
        self.assertEqual(from_dict(json.loads(path.read_text(encoding="utf-8"))), session)
        self.assertEqual(to_dict(generate.load_all(Path(self.tmp.name))[0]), to_dict(session))

    def test_profile_goes_into_the_prompt(self):
        from chunks.interviews import generate
        from chunks.llm import Ollama
        from tests.fake_ollama import FakeOllama

        with FakeOllama() as fake:
            generate.generate_session(self.JOB, "Data Analyst at a refinery", Ollama(host=fake.url, model="fake:latest"))
        self.assertIn("Data Analyst at a refinery", fake.requests[1]["messages"][1]["content"])

    def test_friendly_errors(self):
        from chunks.interviews import generate
        from chunks.llm import Ollama, OllamaError
        from tests.fake_ollama import FakeOllama

        with FakeOllama() as fake:
            with self.assertRaisesRegex(OllamaError, "ollama pull llama3"):
                generate.generate_session(self.JOB, "", Ollama(host=fake.url, model="llama3"))
            self.assertEqual(Ollama(host=fake.url).models(), ["fake:latest"])
        with FakeOllama(bad_json=True) as fake:
            with self.assertRaisesRegex(OllamaError, "JSON válido"):
                generate.generate_session(self.JOB, "", Ollama(host=fake.url, model="fake:latest"))
        with self.assertRaisesRegex(OllamaError, "ollama serve"):
            Ollama(host="http://127.0.0.1:9", model="x", timeout=2).models()
        with self.assertRaisesRegex(ValueError, "curto"):
            generate.generate_session("Dev Python", "", Ollama(host="http://127.0.0.1:9"))

    def test_host_without_scheme(self):
        from chunks.llm import Ollama

        self.assertEqual(Ollama(host="0.0.0.0:11434").host, "http://0.0.0.0:11434")

    def test_fix_markup(self):
        from chunks.interviews.generate import fix_markup, slugify

        self.assertEqual(fix_markup("[[ok]] and ((fill))"), "[[ok]] and ((fill))")
        self.assertEqual(fix_markup("[[broken and ((fill))"), "broken and ((fill))")
        self.assertEqual(slugify("Ação & Co — Sênior Dev"), "acao_co_senior_dev")
