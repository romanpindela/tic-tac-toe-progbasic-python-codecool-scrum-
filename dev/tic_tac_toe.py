from os import system, name
from time import sleep
from random import choice


def cls():
    system('cls' if name == 'nt' else 'clear')


#  A game board
def init_board() -> list:
    board = [
        ['.', '.', '.'],
        ['.', '.', '.'],
        ['.', '.', '.']]
    return board


def get_move(board: list, player: str) -> tuple:
    """ Function where player specifies coordinates as letter and number
    :param board: the game board, check if coordinates are available
    :param player: the current player
    :return: a tuple of two integers: (row, col)"""
    column_id = {"A": 0, "B": 1, "C": 2}
    valid_moves = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
    user_wants_to_quit = False
    while not user_wants_to_quit:
        user_input = input(f"Player: {player} - choose your move (i.e. 'A1') -->: ").upper()
        if user_input == "QUIT":
            user_wants_to_quit = True
        elif user_input not in valid_moves:
            print(f" {user_input} - Not a valid move. Try again!")
        else:
            row, col = column_id[user_input[0]], int(user_input[1]) - 1
            if user_input in valid_moves and board[row][col] == '.':
                return row, col
            else:
                print(f" {user_input} - Cell already taken! Try again!")


def mark(board: list, player: str, row: int, col: int) -> bool:
    """ Function that writes the value of player (X or 0) into the row & col element of board."""

    if board[row][col] == '.':
        board[row][col] = player
    return True


def has_won(board: list, player: str) -> bool:
    """
    Defines all possible winning configurations.
    Returns true if player selects 3 winning coordinates
    """
    win_boards = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
        [board[0][0], board[1][1], board[2][2]]
    ]
    return True if [player, player, player] in win_boards else False


def is_full(board: list) -> bool:
    """ Returns True if there are no empty fields on the board"""
    for col in board:
        if '.' in col:
            return False
    return True


def print_board(board) -> None:
    """
    Prints the board to the screen.
    Players are indicated with X and 0, and empty fields are indicated with dots (.)
    """
    cls()
    row_col_names = {0: "A", 1: "B", 2: "C"}
    print()
    print("1    2   3\n".center(35))
    for row, col in enumerate(board):
        print(f"{row_col_names[row]}     {col[0]}  |  {col[1]} |  {col[2]}".center(30))
        if row <= 1:
            print("----+----+----".center(35))
    print()


def empty_cells(board: list) -> list:
    """
    Checks empty cells on board and returns list of available coordinates
    """
    empty_cells = [[r, c] for r, row in enumerate(board) for c, cell in enumerate(row) if cell == "."]
    return empty_cells


def print_result(board: list, winner: str) -> None:
    """ Prints end game status, winner or a 'tie' """
    if has_won(board=board, player=winner):
        print(f"{winner} has won!")
    elif is_full(board):
        print("It's a tie!")


def change_player(player: str) -> str:
    """ Switches a player """
    if player == player_0:
        return player_X
    else:
        return player_0


def evaluate_end_game(board: list) -> int:
    """
    Returns game state as int
    """
    if has_won(board=board, player=player_X):
        return -1
    elif has_won(board=board, player=player_0):
        return 1
    elif is_full(board=board):
        return 0


def get_ai_move_easy(board: list, player: str) -> tuple:
    """
    Ai move, random choice of coordinates from available moves
    """
    print(f"Player: {player} move".center(30))
    sleep(0.5)
    if len(empty_cells(board=board)) != 0:
        row, col = choice(empty_cells(board=board))
        return row, col


def tictactoe_game(mode: str = 'HUMAN-AI') -> None:
    """
    Main function game. Calls print board function Set up 'X' player as first,
    selects whether ai or player moves, depending on game mode.
    """

    board = init_board()
    print_board(board=board)
    player_turn = player_X
    user_wants_to_quit = False
    move = True
    while evaluate_end_game(board) is None and not user_wants_to_quit:

        if mode == 'HUMAN-HUMAN':
            move = get_move(board=board, player=player_turn)
        elif mode == 'HUMAN-AI-EASY':
            if player_turn == player_X:
                move = get_move(board=board, player=player_turn)
            elif player_turn == player_0:
                move = get_ai_move_easy(board=board, player=player_turn)
        elif mode == 'AI-HUMAN-EASY':
            if player_turn == player_0:
                move = get_move(board=board, player=player_turn)
            elif player_turn == player_X:
                move = get_ai_move_easy(board, player_turn)
        elif mode == 'AI-AI-EASY':
            move = get_ai_move_easy(board=board, player=player_turn)

        if move is not None:
            mark(board=board, player=player_turn, row=move[0], col=move[1])
            print_board(board=board)
            if evaluate_end_game(board=board) is None:
                player_turn = change_player(player=player_turn)
        else:
            # None - znaczy, że jeden z użytkowników chce wyjść (napisał quit)
            user_wants_to_quit = True
    if not user_wants_to_quit:
        print_result(board=board, winner=player_turn)
        user_input = input("Play again (y/n): ").upper()
        if user_input == "Y":
            main_menu()
        else:
            user_wants_to_quit = True


# Welcome screen and select game mode
def main_menu() -> None:
    print("Welcome to Tic-Tac-Toe game!")
    print_board(board=init_board())
    user_wants_to_quit = False
    user_input = input("Choose game mode:\n\n1. HUMAN-HUMAN\n2. HUMAN-AI\n3. AI-HUMAN\n4. AI-AI\n--> ").upper()
    valid_input = ["1", "2", "3", "4", "QUIT"]

    while user_input not in valid_input and not user_wants_to_quit:
        user_input = input("Invalid choice. Try again! -->: ").upper()
    if user_input == "QUIT":
        user_wants_to_quit = True
    if user_input == "1":
        tictactoe_game(mode="HUMAN-HUMAN")
    if user_input == "2":
        tictactoe_game(mode="HUMAN-AI-EASY")
    if user_input == "3":
        tictactoe_game(mode="AI-HUMAN-EASY")
    if user_input == "4":
        tictactoe_game(mode="AI-AI-EASY")

    print("\n")

if __name__ == '__main__':
    player_X = "X"
    player_0 = "0"
    main_menu()