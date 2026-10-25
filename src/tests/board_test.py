import unittest

from src.domain.board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_drop_piece(self):
        row = self.board.drop_piece(3,1)
        self.assertEqual(row,5)
        self.assertEqual(self.board.grid[5][3],1)

    def test_column_full(self):
        for _ in range(6):
            self.board.drop_piece(0,1)
        self.assertTrue(self.board.is_column_full(0))

    def test_horizontal_win(self):
        for col in range(4):
            self.board.drop_piece(col,1)
        self.assertEqual(self.board.check_winner(), 1)

    def test_vertical_win(self):
        for _ in range (4):
            self.board.drop_piece(3,2)
        self.assertEqual(self.board.check_winner(), 2)

if __name__ == '__main__':
    unittest.main()