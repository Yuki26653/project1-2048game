import numpy as np
import random
from typing import List


def slide_left(row: List[int]) -> List[int]:
    """Slide non-zero elements of the row to the left."""
    new_row = [num for num in row if num != 0]
    new_row += [0] * (len(row) - len(new_row))
    return new_row


def slide_right(row: List[int]) -> List[int]:
    """Slide non-zero elements of the row to the right."""
    new_row = [num for num in row if num != 0]
    new_row = [0] * (len(row) - len(new_row)) + new_row
    return new_row


def combine_left(row: List[int]) -> List[int]:
    """Combine adjacent equal elements in the row after sliding left."""
    row = slide_left(row)
    for i in range(len(row) - 1):
        if row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
            row = slide_left(row)
    return row


def combine_right(row: List[int]) -> List[int]:
    """Combine adjacent equal elements in the row after sliding right."""
    row = slide_right(row)
    for i in range(len(row) - 1, 0, -1):
        if row[i] == row[i - 1]:
            row[i] *= 2
            row[i - 1] = 0
            row = slide_right(row)
    return row


def move_left(board: np.ndarray) -> np.ndarray:
    """Move the entire board to the left."""
    new_board = []
    for row in board:
        new_board.append(combine_left(list(row)))  # keep your logic, just make it a plain list
    return np.array(new_board, dtype=int)


def move_right(board: np.ndarray) -> np.ndarray:
    """Move the entire board to the right."""
    new_board = []
    for row in board:
        new_board.append(combine_right(list(row)))
    return np.array(new_board, dtype=int)


def move_up(board: np.ndarray) -> np.ndarray:
    """Move the entire board up."""
    transposed_board = board.T
    moved_board = move_left(transposed_board)
    return moved_board.T


def move_down(board: np.ndarray) -> np.ndarray:
    """Move the entire board down."""
    transposed_board = board.T
    moved_board = move_right(transposed_board)
    return moved_board.T


def random_num() -> int:
    "randomly generate 2 or 4"
    possible_num = (2, 4)  # won't change so tuple
    add_num = random.choice(possible_num)
    return add_num


def insert_num(board: np.ndarray) -> np.ndarray:
    "insert generated number into the board"
    add_num = random_num()  # number to be added
    possible_row = [0, 1, 2, 3]
    possible_col = [0, 1, 2, 3]

    # won't stop until found an empty place
    while True:
        locate_row = random.choice(possible_row)
        locate_col = random.choice(possible_col)  # start with a random column

        if 0 in board[locate_row]:
            while board[locate_row][locate_col] != 0:
                possible_col.remove(locate_col)
                locate_col = random.choice(possible_col)  # choose again until find 0
            break
        else:
            possible_row.remove(locate_row)

    board[locate_row][locate_col] = add_num
    return np.array(board, dtype=int)


def check_change(old_board: np.ndarray, new_board: np.ndarray) -> bool:
    "check if the board has changed after move"
    return not np.array_equal(old_board, new_board)


def keyboard_input(old_board: np.ndarray) -> np.ndarray:
    "get the keyboard input from user"
    valid_keys = ['w', 'a', 's', 'd']
    move_key = input("Please input your move (w/a/s/d): ").strip().lower()

    while move_key not in valid_keys:
        move_key = input("Invalid input. Please input your move (w/a/s/d): ").strip().lower()

    if move_key == 'w':
        new_board = move_up(old_board)
        if check_change(old_board, new_board):
            insert_num(new_board)
        else:
            new_board = old_board

    elif move_key == 'a':
        new_board = move_left(old_board)
        if check_change(old_board, new_board):
            insert_num(new_board)
        else:
            new_board = old_board

    elif move_key == 's':
        new_board = move_down(old_board)
        if check_change(old_board, new_board):
            insert_num(new_board)
        else:
            new_board = old_board

    else:  # 'd'
        new_board = move_right(old_board)
        if check_change(old_board, new_board):
            insert_num(new_board)
        else:
            new_board = old_board

    return new_board


def display(board: np.ndarray) -> None:
    '''increase the readability'''
    SIZE = 4
    CELL_WIDTH = 6  # width per cell

    horizontal_line = "+" + "+".join(["-" * CELL_WIDTH] * SIZE) + "+"

    print(horizontal_line)
    for row in board:
        row_str = "|"
        for cell in row:
            if cell in (0, None):
                row_str += " " * CELL_WIDTH + "|"
            else:
                row_str += f"{int(cell):^{CELL_WIDTH}}|"
        print(row_str)
        print(horizontal_line)


def check_game_over(board: np.ndarray) -> bool:
    'check if the game is over'
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
    return True


def check_win(board: np.ndarray) -> bool:
    'check if the player has won'
    return bool(np.any(board == 2048))


def main() -> None:
    # Here start building the whole game loop
    # initial condition with two numbers
    initial_board = np.zeros((4, 4), dtype=int)
    board_with_num1 = insert_num(initial_board)
    board_with_num2 = insert_num(board_with_num1)
    board = board_with_num2

    print("Welcome to 2048 Game!")

    while check_win(board) == False:
        print("Current Board:")
        display(board)
        board = keyboard_input(board)
        if check_game_over(board):
            print("Game Over! No more moves possible.")
            break


if __name__ == "__main__":
    main()
