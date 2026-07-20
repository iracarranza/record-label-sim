import unittest

from generator import generate_musician


class GeneratorTests(unittest.TestCase):
    def test_generate_musician_assigns_pa_ca_and_stats(self):
        musician = generate_musician()

        self.assertTrue(musician.name)
        self.assertGreaterEqual(musician.pa, 120)
        self.assertLessEqual(musician.pa, 300)
        self.assertGreaterEqual(musician.ca, int(musician.pa * 0.3))
        self.assertLessEqual(musician.ca, int(musician.pa * 0.9))
        self.assertTrue(musician.role)

    def test_generate_musician_respects_pa_stat_cap(self):
        musician = generate_musician(pa=200)
        stat_names = [
            "dexterity",
            "technique",
            "ear_training",
            "music_theory",
            "improvisation",
            "creativity",
            "composition",
            "experimentation",
            "stage_presence",
            "excitement",
            "consistency",
            "nerves",
            "eccentricity",
            "professionalism",
            "ambition",
            "collaboration",
            "ego",
        ]
        total = sum(getattr(musician, name) for name in stat_names)

        self.assertLessEqual(total, musician.pa)
        self.assertGreaterEqual(total, 85)

        for name in stat_names:
            self.assertGreaterEqual(getattr(musician, name), 5)
