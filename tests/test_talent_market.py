import unittest

from game import Game


class TalentMarketTests(unittest.TestCase):
    def test_market_tracks_available_musicians_with_market_fields(self):
        game = Game()

        self.assertGreaterEqual(len(game.talent_market.available), 1)
        musician = game.talent_market.available[0]
        self.assertGreaterEqual(musician.available_weeks, 1)
        self.assertGreaterEqual(musician.asking_salary, 0)
        self.assertGreaterEqual(musician.signing_bonus, 0)
        self.assertGreaterEqual(musician.current_interest, 0)
        self.assertLessEqual(musician.current_interest, 100)

    def test_recruiting_from_market_moves_musician_to_roster(self):
        game = Game()
        market_musician = game.talent_market.available[0]

        recruited = game.recruit_from_market(1)

        self.assertEqual(recruited.name, market_musician.name)
        self.assertNotIn(recruited, game.talent_market.available)
        self.assertIn(recruited, game.musicians)
