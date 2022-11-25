from typing import List, Optional, Tuple

X = "X"
O = "O"


class Board:
    def __init__(self):
        """
        Initialize an empty tic-tac-toe board.
        """
        self._board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def make_move(self, symbol: str, x: int, y: int) -> bool:
        """
        Attempt to make a move on this board with the given symbol at position (x, y).
        :param symbol: X or O
        :param x: An int in (0, 1, 2)
        :param y: An int in (0, 1, 2)
        :return: True if successful, False otherwise
        """
        if self._is_valid_move(symbol, x, y):
            self._board[y][x] = symbol
            return True
        return False

    def are_moves_available(self) -> bool:
        """
        Return True iff there are any empty cells left on this board.
        :return: True if at least one cell is empty, False otherwise
        """
        for row in self._board:
            for cell in row:
                if not cell:
                    return True
        return False

    def is_winner(self, symbol: str):
        """
        Return True iff the player with the given symbol has won the game
        :param symbol: X or O
        :return: True if a line has been made with the given symbol, False otherwise
        """
        return self._is_winner_diagonal(symbol) or \
               self._is_winner_horizontal(symbol) or \
               self._is_winner_vertical(symbol)

    def is_game_over(self):
        return self.is_winner(X) or self.is_winner(O) or not self.are_moves_available()

    def get_all_available_moves(self) -> List[Tuple[int, int]]:
        result = []
        for y in range(len(self._board)):
            for x in range(len(self._board[y])):
                if not self._board[y][x]:
                    result.append((x, y))
        return result

    def _is_valid_move(self, symbol: str, x: int, y: int) -> bool:
        return symbol in (X, O) \
               and 0 <= x <= 2 and 0 <= y <= 2 \
               and not self._board[y][x]

    def _is_winner_diagonal(self, symbol: str) -> bool:
        return self._board[0][0] == self._board[1][1] == self._board[2][2] == symbol or \
               self._board[2][0] == self._board[1][1] == self._board[0][2] == symbol

    def _is_winner_horizontal(self, symbol: str) -> bool:
        return any(self._board[y][0] == self._board[y][1] == self._board[y][2] == symbol for y in (0, 1, 2))

    def _is_winner_vertical(self, symbol: str) -> bool:
        return any(self._board[0][x] == self._board[1][x] == self._board[2][x] == symbol for x in (0, 1, 2))

    def __str__(self) -> str:
        def to_str(symbol: Optional[str]) -> str:
            if symbol is None:
                return " "
            return symbol

        return f"  0 1 2\n" \
               f"0 {to_str(self._board[0][0])}|{to_str(self._board[0][1])}|{to_str(self._board[0][2])}\n" \
               f"  -+-+-\n" \
               f"1 {to_str(self._board[1][0])}|{to_str(self._board[1][1])}|{to_str(self._board[1][2])}\n" \
               f"  -+-+-\n" \
               f"2 {to_str(self._board[2][0])}|{to_str(self._board[2][1])}|{to_str(self._board[2][2])}"
