import unittest
from unittest.mock import patch

from src.core.intelligence import DiceDifficulty


class TestDiceDifficulty(unittest.TestCase):
    def setUp(self):
        self.d = DiceDifficulty()

    def test_available_difficulties(self):
        self.assertEqual(
            self.d.get_available_difficulties(),
            ["noob", "casual", "challenger", "veteran", "elite", "legendary"]
        )

    def test_descriptions(self):
        self.assertTrue("Low skill" in self.d.get_difficulty_description("noob"))
        self.assertTrue("Unknown" in self.d.get_difficulty_description("invalid_mode"))

    @patch("random.choice", return_value=3)
    def test_fixed_roll_patterns(self, _):
        self.assertEqual(self.d.noob(), 3)
        self.assertEqual(self.d.casual(), 3)
        self.assertEqual(self.d.challenger(), 3)
        self.assertEqual(self.d.veteran(), 3)
        self.assertEqual(self.d.elite(), 3)
        self.assertEqual(self.d.legendary(), 3)

    def test_roll_unknown_mode(self):
        with self.assertRaises(ValueError):
            self.d.roll("unknown")

    def test_roll_results_are_int(self):
        for mode in self.d.get_available_difficulties():
            result = self.d.roll(mode)
            self.assertIsInstance(result, int)

    @patch("random.choice", return_value=1)
    def test_roll_bust_rule(self, _):
        for mode in self.d.get_available_difficulties():
            self.assertEqual(self.d.roll(mode), 1)