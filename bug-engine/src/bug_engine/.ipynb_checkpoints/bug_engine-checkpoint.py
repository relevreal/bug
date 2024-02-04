import bisect
from copy import copy
from enum import Enum
import array
from collections.abc import Iterable, Generator 
from itertools import chain


# class Bug:
#     def __init__(self, hexagons: Iterable[int]):
#         self.hexagons = set(hexagons)
#         self.id = None


def get_hex_num(board_size: int) -> int:
    if board_size < 2:
        raise ValueError('board size has to be at least 2')
    # start with the middle row
    hex_num = 2 * board_size - 1
    for row_i in range(board_size - 1):
        row_size = board_size + row_i
        # times 2 to account of mirror row on the other half of the board
        hex_num += 2 * row_size
    return hex_num


# class BugEngine:
#     def __init__(self, board_size: int):
#         self.hex_num = get_hex_num(board_size)
#         self.board = array.array("B", (0 for _ in range(self.hex_num)))


def is_on_upper_border(board_size: int, hex_idx: int) -> bool:
    if hex_idx >= board_size:
        return False
    return True

    
def is_on_lower_border(board_size: int, hex_idx: int) -> bool:
    hex_num = get_hex_num(board_size)
    if hex_idx + board_size < hex_num:
        return False
    return True


def is_on_left_border(board_size: int, hex_idx: int) -> bool:
    candidate = 0
    if hex_idx < candidate:
        return False
    if hex_idx == candidate:
        return True
    increasing = range(board_size, 2 * board_size - 1)
    decreasing = range(2 * board_size - 1, board_size, -1)
    for inc in  chain(increasing, decreasing):
        candidate += inc
        if hex_idx == candidate:
            return True
        if hex_idx < candidate:
            return False
    return False
        

def is_on_right_border(board_size: int, hex_idx: int) -> bool:
    candidate = board_size - 1 
    if hex_idx < candidate:
        return False
    if hex_idx == candidate:
        return True
    increasing = range(board_size + 1, 2 * board_size - 1)
    decreasing = range(2 * board_size - 1, board_size - 1, -1)
    for inc in  chain(increasing, decreasing):
        candidate += inc
        if hex_idx == candidate:
            return True
        if hex_idx < candidate:
            return False
    return False


def make_row_idxs(board_size: int) -> Generator[int]:
    row_idx = board_size - 1
    longest_row = 2 * board_size - 1
    increasing = range(board_size + 1, longest_row)
    decreasing = reversed(increasing)
    yield row_idx
    for inc in  increasing:
        row_idx += inc
        yield row_idx
    row_idx += longest_row
    yield row_idx
    for dec in decreasing:
        row_idx += dec
        yield row_idx


def get_hex_row_idx(row_idxs, hex_idx) -> int:
    return bisect.bisect_left(row_idxs, hex_idx)


def make_row_sizes(board_size: int) -> Generator[int]:
    longest_row = 2 * board_size - 1
    increasing = range(board_size, longest_row)
    decreasing = reversed(increasing)
    for row_size in  chain(increasing, [longest_row], decreasing):
        yield row_size


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UPPER_LEFT = 3
    UPPER_RIGHT = 4
    LOWER_LEFT = 5
    LOWER_RIGHT = 6


def get_hex_from_direction(board_size: int, hex_idx: int, direction: Direction) -> int:
    if direction == Direction.LEFT:
        # print('Direction.LEFT')
        return hex_idx - 1
    if direction ==  Direction.RIGHT:
        # print('Direction.RIGHT')
        return hex_idx + 1

    hex_num = get_hex_num(board_size)
    longest_row = 2 * board_size - 1
    is_first_half = hex_idx < (hex_num - longest_row) // 2
    is_second_half = hex_idx >= (hex_num - longest_row) // 2 + longest_row

    row_idxs = tuple(make_row_idxs(board_size))
    row_sizes = tuple(make_row_sizes(board_size))
    hex_row = get_hex_row_idx(row_idxs, hex_idx)
    row_size = row_sizes[hex_row]

    if direction == Direction.UPPER_LEFT:
        # print('Direction.UPPER_LEFT')
        if is_second_half:
            return hex_idx - row_size - 1
        return hex_idx - row_size
    if direction == Direction.UPPER_RIGHT:
        # print('Direction.UPPER_RIGHT')
        if not is_second_half:
            return hex_idx - row_size + 1
        return hex_idx - row_size
    if direction == Direction.LOWER_LEFT:
        # print('Direction.LOWER_LEFT')
        if is_first_half:
            return hex_idx + row_size
        return hex_idx + row_size - 1
    # Direction.LOWER_RIGHT
    # print('Direction.LOWER_RIGHT', is_first_half)
    if is_first_half:
        return hex_idx + row_size + 1
    return hex_idx + row_size


def get_neighbours(board_size: int, hex_idx: int) -> Generator[int]:
    hex_num = get_hex_num(board_size)
    longest_row = 2 * board_size - 1

    is_up = is_on_upper_border(board_size, hex_idx)
    is_down = is_on_lower_border(board_size, hex_idx)
    is_left = is_on_left_border(board_size, hex_idx)
    is_right = is_on_right_border(board_size, hex_idx)
    is_first_half = hex_idx < (hex_num - longest_row) // 2
    is_second_half = hex_idx >= (hex_num - longest_row) // 2 + longest_row

    if not is_up and (not is_left or is_second_half):
        yield get_hex_from_direction(board_size, hex_idx, Direction.UPPER_LEFT)
    if not is_up and (not is_right or is_second_half):
        yield get_hex_from_direction(board_size, hex_idx, Direction.UPPER_RIGHT)
    if not is_left:
        yield get_hex_from_direction(board_size, hex_idx, Direction.LEFT)
    if not is_right:
        yield get_hex_from_direction(board_size, hex_idx, Direction.RIGHT)
    if not is_down and (not is_left or is_first_half):
        yield get_hex_from_direction(board_size, hex_idx, Direction.LOWER_LEFT)
    if not is_down and (not is_right or is_first_half):
        yield get_hex_from_direction(board_size, hex_idx, Direction.LOWER_RIGHT)


def get_forward_neighbours(board_size: int, hex_idx: int) -> Generator[int]:
    hex_num = get_hex_num(board_size)
    longest_row = 2 * board_size - 1

    is_down = is_on_lower_border(board_size, hex_idx)
    is_left = is_on_left_border(board_size, hex_idx)
    is_right = is_on_right_border(board_size, hex_idx)
    is_first_half = hex_idx < (hex_num - longest_row) // 2

    if not is_right:
        yield get_hex_from_direction(board_size, hex_idx, Direction.RIGHT)
    if not is_down and (not is_left or is_first_half):
        yield get_hex_from_direction(board_size, hex_idx, Direction.LOWER_LEFT)
    if not is_down and (not is_right or is_first_half):
        yield get_hex_from_direction(board_size, hex_idx, Direction.LOWER_RIGHT)


# TODO  
def bug_generator(board_size: int, bug_size: int):
    hex_num = get_hex_num(board_size)
    for i in range(hex_num):
        yield from _bug_generator(board_size, bug_size - 1, [i])


def _bug_generator(board_size: int, bug_size: int, bug: list[int]) -> Generator[list[int]]:
    if bug_size == 0:
        yield bug
    else:
        for neighbour in get_forward_neighbours(board_size, bug[-1]):
            bug_len = len(bug)
            bug.append(neighbour)
            for b in _bug_generator(board_size, bug_size - 1, bug):
                yield b
                bug = bug[:bug_len]
             

# TODO  
def are_isomorphic(board_size: int, bug_1, bug_2) -> bool:
    return False