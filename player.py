from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional, Tuple

from board import Board, X, O


class Player(ABC):
    def __init__(self, symbol):
        """
        Initialize this player to use the given symbol
        :param symbol: X or O
        """
        if symbol not in (X, O):
            raise ValueError(f"Symbol must be {X} or {O}")
        self._symbol = symbol

    def is_winner(self, board: Board) -> bool:
        """
        Return True iff this player is the winner of the game on the given board.
        :param board: The tic-tac-toe board being played on
        :return: True if this player has made a line, False otherwise
        """
        return board.is_winner(self._symbol)

    @abstractmethod
    def make_move(self, board: Board) -> None:
        pass


class HumanPlayer(Player):
    """
    A human player. Moves are made by prompting the user to select a move and executing it.
    """

    def make_move(self, board: Board) -> None:
        """
        Prompt the user to make a move, then execute it. If the user does not enter a valid move, this will repeat the
        prompt until a valid move has been selected.
        :param board: The board being played on
        """
        is_valid_move = self._prompt_for_move(board)
        while not is_valid_move:
            print("That is not recognized as a valid move.")
            is_valid_move = self._prompt_for_move(board)

    def _prompt_for_move(self, board: Board) -> bool:
        raw_input = input("Please specify a move in format x,y: ")
        coords = raw_input.split(",")
        if len(coords) != 2:
            return False
        x, y = (coord.strip() for coord in coords)
        if not x.isnumeric or not y.isnumeric:
            return False
        return board.make_move(self._symbol, int(x), int(y))


class ComputerPlayer(Player):
    """
    A computer player. This player uses the minimax algorithm to select an optimal move, and therefore, should be
    unbeatable.
    """

    def __init__(self, symbol):
        super().__init__(symbol)
        self._opponent_symbol = O if symbol == X else X

    def make_move(self, board: Board) -> None:
        """
        Calculate the best move to make in the board's current state, then execute that move.
        :param board: The board being played on
        """
        print("Thinking of move...")
        _, (x, y) = self._minimax(board, True, 0)
        board.make_move(self._symbol, x, y)
        print("Move completed")

    def _minimax(self, board: Board, is_this_player: bool, depth: int) -> Tuple[int, Optional[Tuple[int, int]]]:
        if board.is_game_over():
            if self.is_winner(board):
                return 10 - depth, None
            elif board.is_winner(self._opponent_symbol):
                return -10 + depth, None
            return 0, None

        current_symbol = self._symbol if is_this_player else self._opponent_symbol
        best_score = None
        best_move = None
        for x, y in board.get_all_available_moves():
            board_copy = deepcopy(board)
            board_copy.make_move(current_symbol, x, y)
            score, _ = self._minimax(board_copy, not is_this_player, depth + 1)
            if is_this_player:
                # Best score is the maximum score
                if best_score is None or score > best_score:
                    best_score = score
                    best_move = (x, y)
            else:
                # Best score is the minimum score
                if best_score is None or score < best_score:
                    best_score = score
                    best_move = (x, y)

        return best_score, best_move
