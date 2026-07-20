import unittest

from game import Game


class GameSystemTests(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_next_week_stores_event_in_inbox(self):
        event = self.game.next_week()

        self.assertEqual(self.game.week, 2)
        self.assertEqual(len(self.game.inbox), 1)
        self.assertEqual(event.week, 2)
        self.assertIn("Week 2", event.message)

    def test_help_lists_supported_commands(self):
        help_text = self.game.show_help()

        self.assertIn("help", help_text)
        self.assertIn("roster", help_text)
        self.assertIn("inbox", help_text)
        self.assertIn("musician <number>", help_text)

    def test_musician_inspection_shows_key_details(self):
        details = self.game.show_musician(1)

        self.assertIn("Cedric", details)
        self.assertIn("CA", details)
        self.assertIn("PA", details)
        self.assertIn("Dexterity", details)
        self.assertIn("Stage Presence", details)

    def test_recruit_adds_new_musician(self):
        recruited = self.game.recruit_from_market(1)

        self.assertEqual(recruited.name, recruited.name)
        self.assertEqual(len(self.game.musicians), 4)
        self.assertIn(recruited.name, self.game.show_roster())

    def test_game_uses_genre_and_ensemble_template_for_starting_roster(self):
        game = Game(genre="Pop Punk", ensemble_size="Duo")

        self.assertEqual(game.genre, "Pop Punk")
        self.assertEqual(game.ensemble_size, "Duo")
        self.assertEqual(len(game.musicians), 2)
        self.assertEqual(game.bands[0].genre, "Pop Punk")
