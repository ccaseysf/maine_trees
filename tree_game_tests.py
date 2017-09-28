import tree_game_lib

board1 = [
    [tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_EMPTY],
    [tree_game_lib.BOARD_TENT, tree_game_lib.BOARD_EMPTY, tree_game_lib.BOARD_TREE],
    [tree_game_lib.BOARD_TENT, tree_game_lib.BOARD_EMPTY, tree_game_lib.BOARD_TENT],
    [tree_game_lib.BOARD_TENT, tree_game_lib.BOARD_TENT, tree_game_lib.BOARD_TENT],
]

board2 = [
    [tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TENT],
    [tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TENT, tree_game_lib.BOARD_TREE],
    [tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_EMPTY, tree_game_lib.BOARD_TENT],
]


def test_validate():
    # row is too large
    try:
        tree_game_lib.validate(board1, row=len(board1))
    except tree_game_lib.OutOfRange:
        pass
    else:
        print("validate(board1, row=len(board1)) returned, expected OutOfRange exception")
        return False

    # col is too large
    try:
        tree_game_lib.validate(board1, col=len(board1[0]))
    except tree_game_lib.OutOfRange:
        pass
    else:
        print("validate(board1, col=len(board1[0])) returned, expected OutOfRange exception")
        return False

    # Neither row nor col are set
    try:
        tree_game_lib.validate(board1)
    except tree_game_lib.OutOfRange:
        pass
    else:
        print("validate(board1) returned, expected OutOfRange exception")
        return False

    return True


def test_get():
    square = tree_game_lib.get(board1, -1, 0)
    if square != tree_game_lib.BOARD_OUT_OF_BOUNDS:
        print("get(board1, -1, 0) returned %s, expected BOARD_OUT_OF_BOUNDS", square)
        return False

    square = tree_game_lib.get(board1, 0, 0)
    if square != board1[0][0]:
        print("get(board1, 0, 0) returned %s, expected %s" % (square, board1[0][0]))
        return False

    return True


def test_percent_chance():
    for i in range(1000):
        if tree_game_lib.percent_chance(0):
            print("percent_chance(0) returned True, expected False")
            return False

    for i in range(1000):
        if not tree_game_lib.percent_chance(100):
            print("percent_chance(100) returned False, expected True")
            return False

    for percent in [5, 25, 55, 90]:
        hits = 0
        tries = 10000
        for i in range(tries):
            if tree_game_lib.percent_chance(percent):
                hits += 1
        print("INFO: percent_chance(%d) -> %d%%" % (percent, 100 * hits / tries + .5))

    return True


def test_is_tent():
    if not tree_game_lib.is_tent(board1, 1, 0):
        print("is_tent(BOARD_TENT) returned False, expected True")
        return False

    if tree_game_lib.is_tent(board1, 0, 0):
        print("is_tent(BOARD_TREE) returned True, expected False")
        return False

    if tree_game_lib.is_tent(board1, 0, -1):
        print("is_tent(BOARD_TREE) returned True, expected False")
        return False

    return True


def test_count_tents():
    for r in range(len(board1)):
        count = tree_game_lib.count_tents(board1, row=r)
        if count != r:
            print("count_tents(board1, %d) returned %d expected %d" % (r, count, r))
            return False

    for c in range(len(board2[0])):
        count = tree_game_lib.count_tents(board2, col=c)
        if count != c:
            print("count_tents(board2, %d) returned %d expected %d" % (c, count, c))
            return False

    return True


def test_can_place_tent():
    r = 0
    c = 0
    if tree_game_lib.can_place_tent(board1, r, c):
        print("can_place_tent(board1, %d, %d) returned True, expected False" % (r, c))

    r = 2
    c = 1
    if tree_game_lib.can_place_tent(board1, r, c):
        print("can_place_tent(board1, %d, %d) returned True, expected False" % (r, c))

    r = 0
    c = 2
    if not tree_game_lib.can_place_tent(board1, r, c):
        print("can_place_tent(board1, %d, %d) returned False, expected True" % (r, c))

    return True


def test_place_tree_and_tent():
    board = [
        [tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TREE],
        [tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TREE],
        [tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TREE, tree_game_lib.BOARD_TREE],
    ]

    for r, c in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
        row = 1 + r
        col = 1 + c
        board[1][1] = tree_game_lib.BOARD_EMPTY
        board[row][col] = tree_game_lib.BOARD_EMPTY
        tree_game_lib.place_tree_and_tent(board, 1, 1)
        if not tree_game_lib.is_tent(board, row, col):
            print("place_tree_and_tent(board, 1, 1) did not place a tent at %d,%d" % (row, col))
            return False
        board[row][col] = tree_game_lib.BOARD_TREE

    return True


def test_create_board():
    # TODO: write a test
    return True


def test_create_guess_board():
    guess = tree_game_lib.create_guess_board(board1)

    # Make a copy of board1 that has no tents
    board = tree_game_lib.copy_board(board1)
    for r in range(len(board)):
        for c in range(len(board[0])):
            if tree_game_lib.is_tent(board, r, c):
                board[r][c] = tree_game_lib.BOARD_EMPTY

    # Compare the copy with guess
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] != guess[r][c]:
                print("board[%d][%d] != guess[%d][%d] %s != %s" % (r, c, r, c, board[r][c], guess[r][c]))
                return False

    return True


if not test_validate():
    exit(1)
if not test_get():
    exit(1)
if not test_percent_chance():
    exit(1)
if not test_is_tent():
    exit(1)
if not test_count_tents():
    exit(1)
if not test_can_place_tent():
    exit(1)
if not test_place_tree_and_tent():
    exit(1)
if not test_create_board():
    exit(1)
if not test_create_guess_board():
    exit(1)
