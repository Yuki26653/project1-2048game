import random
import numpy as np

from game_2048 import (
    slide_left,
    slide_right,
    combine_left,
    combine_right,
    move_left,
    move_right,
    move_up,
    move_down,
    insert_num,
    check_game_over,
    check_win,
)


def test_slide_left():
    assert slide_left([0, 2, 0, 4]) == [2, 4, 0, 0]


def test_slide_right():
    assert slide_right([0, 2, 0, 4]) == [0, 0, 2, 4]


def test_combine_left_simple():
    assert combine_left([2, 2, 0, 0]) == [4, 0, 0, 0]


def test_combine_right_simple():
    assert combine_right([0, 0, 2, 2]) == [0, 0, 0, 4]


def test_move_left_basic_board():
    board = np.array([
        [0, 2, 2, 0],
        [4, 0, 4, 0],
        [2, 2, 2, 2],
        [0, 0, 0, 0],
    ])
    moved = move_left(board)
    expected = np.array([
        [4, 0, 0, 0],
        [8, 0, 0, 0],
        [4, 4, 0, 0],
        [0, 0, 0, 0],
    ])
    assert np.array_equal(moved, expected)


def test_move_up_down_column_merge():
    board = np.array([
        [2, 0, 0, 0],
        [2, 0, 0, 0],
        [4, 0, 0, 0],
        [4, 0, 0, 0],
    ])
    up = move_up(board)
    down = move_down(board)
    assert np.array_equal(up[:, 0], np.array([4, 8, 0, 0]))
    assert np.array_equal(down[:, 0], np.array([0, 0, 4, 8]))


def test_insert_num_adds_one_tile():
    random.seed(0)
    board = np.zeros((4, 4), dtype=int)
    before = np.count_nonzero(board)
    insert_num(board)
    after = np.count_nonzero(board)
    assert after == before + 1
    assert set(board.flatten()).issubset({0, 2, 4})


def test_game_over_true_when_no_moves():
    board = np.array([
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ])
    assert check_game_over(board) is True


def test_game_over_false_when_merge_exists():
    board = np.array([
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 4],
    ])
    assert check_game_over(board) is False


def test_check_win():
    board = np.zeros((4, 4), dtype=int)
    board[0, 0] = 2048
    assert check_win(board) is True
