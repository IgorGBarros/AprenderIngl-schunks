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
        self.assertEqual(p.pt, "Pode me ver um café, por favor?")

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

    def test_signature_is_introspectable(self):
        self.assertEqual(chunks.let_me_loop_in.pattern, "let_me_loop_in(person, topic)")


class TestLibrary(unittest.TestCase):
    def test_every_chunk_is_consistent(self):
        for c in chunks.registry().values():
            with self.subTest(chunk=c.name):
                pt_slots = {f for _, f, _, _ in string.Formatter().parse(c.pt) if f}
                self.assertEqual(pt_slots, set(c.slots), "tradução usa variáveis diferentes")
                self.assertTrue(set(c.slots) - set(c.defaults) <= set(c.example) <= set(c.slots))
                self.assertIn("[[", c.template)
                demo = c.demo()
                self.assertNotIn("[[", demo.en)
                self.assertIn("{{c1::", demo.cloze)

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


if __name__ == "__main__":
    unittest.main()
