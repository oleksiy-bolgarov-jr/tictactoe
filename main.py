from board import Board, X, O
from player import Player, HumanPlayer, ComputerPlayer


def play_one_round():
    board = Board()
    player1 = get_player(1)
    player2 = get_player(2)

    current_player = player1
    while not board.is_game_over():
        print(board)
        if current_player == player1:
            print("Player 1's turn")
        else:
            print("Player 2's turn")
        current_player.make_move(board)

        if current_player == player1:
            current_player = player2
        else:
            current_player = player1

    print(board)
    if player1.is_winner(board):
        print("Player 1 wins!")
    elif player2.is_winner(board):
        print("Player 2 wins!")
    else:
        print("The game is a draw.")


def get_player(player_num: int) -> Player:
    if player_num not in (1, 2):
        raise ValueError("player_num must be 1 or 2")
    symbol = X if player_num == 1 else O

    response = input(f"Player {player_num}: human or computer? (Type 1 for human, 2 for computer): ")
    if response.strip().startswith("1"):
        return HumanPlayer(symbol)

    return ComputerPlayer(symbol)


while True:
    play_one_round()
    play_again = input("Would you like to play again? (Y/N): ")
    if not play_again.strip().lower().startswith("y"):
        break
