import unittest
from tictactoe import Board


class TestBoard(unittest.TestCase):

    def test_init(self):
        board = Board()
        self.assertEqual(board.state, [' '] * 9)

    def test_init_initial_state(self):
        board = Board(['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'O'])
        self.assertEqual(board.state, ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'O'])

    def test_available_moves_empty(self):
        board = Board()
        self.assertEqual(board.available_moves, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_available_moves_full(self):
        board = Board(['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'O'])
        self.assertEqual(board.available_moves, [])

    def test_available_moves_partially_full(self):
        board = Board(['X', 'O', ' ', 'X', ' ', 'O', 'O', 'X', 'O'])
        self.assertEqual(board.available_moves, [3, 5])

    def test_full_when_empty(self):
        board = Board()
        self.assertFalse(board.full)

    def test_full_when_full(self):
        board = Board(['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'O'])
        self.assertTrue(board.full)

    def test_full_when_partially_filled(self):
        board = Board(['X', 'O', ' ', 'X', ' ', 'O', ' ', 'X', 'O'])
        self.assertFalse(board.full)

    def test_winner_when_empty(self):
        board = Board()
        self.assertFalse(board.check_winner())

    def test_winner_row1(self):
        board = Board(['X', 'X', 'X', 'O', 'O', ' ', 'O', ' ', ' '])
        self.assertEqual(board.check_winner(), 'X')

    def test_winner_row2(self):
        board = Board(['X', ' ', 'X', 'O', 'O', 'O', 'O', ' ', 'X'])
        self.assertEqual(board.check_winner(), 'O')

    def test_winner_row3(self):
        board = Board(['O', 'O', ' ', 'O', ' ', ' ', 'X', 'X', 'X'])
        self.assertEqual(board.check_winner(), 'X')

    def test_winner_col1(self):
        board = Board(['X', 'O', ' ', 'X', ' ', 'O', 'X', 'O', 'X'])
        self.assertEqual(board.check_winner(), 'X')

    def test_winner_col2(self):
        board = Board(['X', 'O', ' ', ' ', 'O', 'O', 'X', 'O', 'X'])
        self.assertEqual(board.check_winner(), 'O')

    def test_winner_col3(self):
        board = Board(['O', 'O', 'X', ' ', 'X', 'O', 'X', ' ', 'X'])
        self.assertEqual(board.check_winner(), 'X')

    def test_winner_diag1(self):
        board = Board(['X', 'O', 'O', ' ', 'X', ' ', ' ', 'O', 'X'])
        self.assertEqual(board.check_winner(), 'X')

    def test_winner_diag2(self):
        board = Board(['X', 'O', 'O', 'X', 'O', ' ', 'O', ' ', 'X'])
        self.assertEqual(board.check_winner(), 'O')

    def test_get_position_empty(self):
        board = Board()
        self.assertEqual(board[0], ' ')

    def test_get_position_filled(self):
        board = Board(['X', 'O', ' ', 'X', ' ', 'O', 'O', 'X', 'O'])
        self.assertEqual(board[0], 'X')
        self.assertEqual(board[1], 'O')
        self.assertEqual(board[2], ' ')

    def test_position_assignment(self):
        board = Board()
        self.assertEqual(board[0], ' ')
        board[0] = 'X'
        self.assertEqual(board[0], 'X')

    def test_iter(self):
        board = Board(['X', 'O', ' ', 'X', ' ', 'O', 'O', 'X', 'O'])
        iterator = iter(board)
        self.assertEqual(next(iterator), 'X')
        self.assertEqual(next(iterator), 'O')
        self.assertEqual(next(iterator), ' ')
        self.assertEqual(next(iterator), 'X')
        self.assertEqual(next(iterator), ' ')
        self.assertEqual(next(iterator), 'O')
        self.assertEqual(next(iterator), 'O')
        self.assertEqual(next(iterator), 'X')
        self.assertEqual(next(iterator), 'O')
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_len(self):
        board = Board()
        self.assertEqual(len(board), 9)

    def test_str_empty(self):
        board = Board()
        board_string = '   |   |  \n-----------\n   |   |  \n-----------\n   |   |  '
        self.assertEqual(str(board), board_string)

    def test_str_filled(self):
        board = Board(['X', 'O', ' ', 'X', ' ', 'O', 'O', 'X', 'O'])
        board_string = ' X | O |  \n-----------\n X |   | O\n-----------\n O | X | O'
        self.assertEqual(str(board), board_string)

if __name__ == "__main__":
    unittest.main()
