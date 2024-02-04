import pytest

from bug_engine.bug_engine import (
    is_on_left_border,
    is_on_right_border,
    is_on_upper_border,
    is_on_lower_border,
    get_hex_num,
    make_row_idxs,
    get_hex_row_idx,
    make_row_sizes,
    get_neighbours,
)


@pytest.mark.parametrize('given,expected', [
    (2, 7),
    (3, 19),
    (4, 37),
    (5, 61),
    (6, 91),
])
def test_get_hex_num_ok(given: int, expected: int) -> None:
    result = get_hex_num(given)
    assert result == expected


@pytest.mark.parametrize('given', [-1, 0, 1])
def test_get_hex_num_fail(given: int) -> None:
    with pytest.raises(ValueError) as err:
        _ = get_hex_num(given)
    assert str(err.value) == 'board size has to be at least 2'


@pytest.mark.parametrize('board_size,on_border,is_on_border', [
    (3, (0, 3, 7, 12, 16), is_on_left_border),
    (3, (2, 6, 11, 15, 18), is_on_right_border),
    (3, (0, 1, 2), is_on_upper_border),
    (3, (16, 17, 18), is_on_lower_border),
    (4, (0, 4, 9, 15, 22, 28, 33), is_on_left_border),
    (4, (3, 8, 14, 21, 27, 32, 36), is_on_right_border),
    (4, (0, 1, 2, 3), is_on_upper_border),
    (4, (33, 34, 35, 36), is_on_lower_border),
    (5, (0, 5, 11, 18, 26, 35, 43, 50, 56), is_on_left_border),
    (5, (4, 10, 17, 25, 34, 42, 49, 55, 60), is_on_right_border),
    (5, (0, 1, 2, 3, 4), is_on_upper_border),
    (5, (56, 57, 58, 59, 60), is_on_lower_border),
])
def test_is_on_border_ok(board_size: int, on_border: tuple[int], is_on_border) -> None:
    for hex_idx in on_border:
        assert is_on_border(board_size, hex_idx) is True

    hex_num = get_hex_num(board_size)
    not_on_border_iter = (
        hex_idx 
        for hex_idx in range(hex_num) 
        if hex_idx not in on_border
    )

    for hex_idx in not_on_border_iter:
        assert is_on_border(board_size, hex_idx) is False


@pytest.mark.parametrize('board_size,expected', [
    (3, (2, 6, 11, 15)),
    (4, (3, 8, 14, 21, 27, 32)),
    (5, (4, 10, 17, 25, 34, 42, 49, 55)),
])
def test_make_row_idxs_ok(board_size: int, expected: tuple[int]) -> None:
    result = tuple(make_row_idxs(board_size))
    assert result == expected


@pytest.mark.parametrize('hex_idx,row_idxs,expected', [
    (0, (2, 6, 11, 15), 0),
    (2, (2, 5, 9, 14), 0),
    (4, (2, 5, 9, 14), 1),
    (8, (2, 5, 9, 14), 2),
    (10, (2, 5, 9, 14), 3),
    (16, (2, 5, 9, 14), 4),
])
def test_get_hex_row_idx_ok(hex_idx: int, row_idxs: tuple[int], expected: int) -> None:
    result = get_hex_row_idx(row_idxs, hex_idx)
    assert result == expected
    

@pytest.mark.parametrize('board_size,expected', [
    (3, (3, 4, 5, 4, 3)),
    (4, (4, 5, 6, 7, 6, 5, 4)),
    (5, (5, 6, 7, 8, 9, 8, 7, 6, 5)),
])
def test_make_row_sizes_ok(board_size: int, expected: tuple[int]) -> None:
    result = tuple(make_row_sizes(board_size))
    assert result == expected


@pytest.mark.parametrize('board_size,hex_idx,expected', [
    # board size 3
    (3, 0, (1, 3, 4)),
    (3, 1, (0, 2, 4, 5)),
    (3, 2, (1, 5, 6)),
    (3, 3, (0, 4, 7, 8)),
    (3, 4, (0, 1, 3, 5, 8, 9)),
    (3, 5, (1, 2, 4, 6, 9, 10)),
    (3, 6, (2, 5, 10, 11)),
    (3, 7, (3, 8, 12)),
    (3, 8, (3, 4, 7, 9, 12, 13)),
    (3, 9, (4, 5, 8, 10, 13, 14)),
    (3, 10, (5, 6, 9, 11, 14, 15)),
    (3, 11, (6, 10, 15)),
    (3, 12, (7, 8, 13, 16)),
    (3, 13, (8, 9, 12, 14, 16, 17)),
    (3, 14, (9, 10, 13, 15, 17, 18)),
    (3, 15, (10, 11, 14, 18)),
    (3, 16, (12, 13, 17)),
    (3, 17, (13, 14, 16, 18)),
    (3, 18, (14, 15, 17)),
    # board size 4
    (4, 0, (1, 4, 5)),
    (4, 3, (2, 7, 8)),
    (4, 9, (4, 10, 15, 16)),
    (4, 14, (8, 13, 20, 21)),
    (4, 15, (9, 16, 22)),
    (4, 18, (11, 12, 17, 19, 24, 25)),
    (4, 21, (14, 20, 27)),
    (4, 22, (15, 16, 23, 28)),
    (4, 27, (20, 21, 26, 32)),
    (4, 33, (28, 29, 34)),
    (4, 36, (31, 32, 35)),
    # board size 5
    (5, 0, (1, 5, 6)),
    (5, 4, (3, 9, 10)),
    (5, 18, (11, 19, 26, 27)),
    (5, 25, (17, 24, 33, 34)),
    (5, 26, (18, 27, 35)),
    (5, 30, (21, 22, 29, 31, 38, 39)),
    (5, 34, (25, 33, 42)),
    (5, 35, (26, 27, 36, 43)),
    (5, 42, (33, 34, 41, 49)),
    (5, 56, (50, 51, 57)),
    (5, 60, (54, 55, 59)),
])
def test_get_neighbours_ok(board_size: int, hex_idx: int, expected: tuple[int]) -> None:
    print()
    result = tuple(get_neighbours(board_size, hex_idx))
    assert result == expected


@pytest.mark.parametrize('board_size,bug_size,expected', [
    (3, 3, [
        [0, 1, 2],
        
    ])
])
def test_bug_generator_ok(board_size: int, bug_size: int, expected: list[list[int]]) -> None:
    
    

# def test_are_isomorphic():
#     board_size = 3

#     bug_1 = Bug((0, 1, 2)) 
#     bug_2 = Bug((1, 2, 3))
#     bug_3 = Bug((0, 1, 3))

#     assert are_isomorphic(board_size, bug_1, bug_2)
#     assert are_isomorphic(board_size, bug_1, bug_2)
#     assert not are_isomorphic(board_size, bug_1, bug_3)
#     assert not are_isomorphic(board_size, bug_2, bug_3)
