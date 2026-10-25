import unittest
from src.services.game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_initial_state(self):
        self.assertEqual(self.game.current_player,1)
        self.assertFalse(self.game.game_over)

    def test_valid_move(self):
        result= self.game.make_move(3)
        self.assertTrue(result['success'])
        self.assertEqual(self.game.current_player,2)

    def test_invalid_column(self):
        result= self.game.make_move(8)
        self.assertFalse(result['success'])

    def test_computer_blocks(self):
        self.game.make_move(0)
        self.game.current_player = 1
        self.game.make_move(1)
        self.game.current_player = 1
        self.game.make_move(2)

        # P1 can win at column 3 , computer should block
        self.game.current_player = 2
        move= self.game.get_computer_move()
        self.assertEqual(move, 3)

if __name__ == '__main__':
    unittest.main()
