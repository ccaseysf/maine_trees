import tree_game_lib
import random


def get(trees, row, col):
    """
    Args:
        trees - game board
        row - any integer
        col - any integer

    Returns:
        returns a character
        if row, col is on the board, the character at that location is returned
        if row, col is not on the board, the character for out of bounds is returned
    """
    if row < 0 or row > len(trees)-1:
        return tree_game_lib.BOARD_OUT_OF_BOUNDS
    if col < 0 or col > len(trees[0])-1:
        return tree_game_lib.BOARD_OUT_OF_BOUNDS
    return trees[row][col]


def can_place_tent(trees, row, col):
    """
    tents - go next to tree - one tent per tree, if square around tree, and on board
    Includes the diagonal check for tent placement

    # square needs to be empty, not next another tent, on the board

    args:
        trees - game board
        row - row on the game board
        col - column on the game board

    returns:
        boolean - true or false
            True - legal to place tent at row, col
            False - illegal to place tent at row, col
    """
    return (
        get(trees, row, col) == tree_game_lib.BOARD_EMPTY and
        get(trees, row - 1, col - 1) != tree_game_lib.BOARD_TENT and
        get(trees, row - 1, col - 0) != tree_game_lib.BOARD_TENT and
        get(trees, row - 1, col + 1) != tree_game_lib.BOARD_TENT and
        get(trees, row - 0, col - 1) != tree_game_lib.BOARD_TENT and
        get(trees, row - 0, col + 1) != tree_game_lib.BOARD_TENT and
        get(trees, row + 1, col - 1) != tree_game_lib.BOARD_TENT and
        get(trees, row + 1, col - 0) != tree_game_lib.BOARD_TENT and
        get(trees, row + 1, col + 1) != tree_game_lib.BOARD_TENT
    )


def place_tent_and_tree(trees, row, col):
    """Place a tent next to a tree.

    Args:
        trees - game board
        row - integer
        col - integer

    Returns:
        returns a character of
    """
    if trees[row][col] != tree_game_lib.BOARD_EMPTY:
        return

    choices = []

    if can_place_tent(trees, row - 1, col - 0):
        choices.append([row - 1, col - 0])
    if can_place_tent(trees, row - 0, col - 1):
        choices.append([row - 0, col - 1])
    if can_place_tent(trees, row - 0, col + 1):
        choices.append([row - 0, col + 1])
    if can_place_tent(trees, row + 1, col - 0):
        choices.append([row + 1, col - 0])

    if len(choices) <= 0:
        return

    choice = random.randint(0, len(choices)-1)
    r = choices[choice][0]
    c = choices[choice][1]

    trees[r][c] = tree_game_lib.BOARD_TENT
    trees[row][col] = tree_game_lib.BOARD_TREE


def create_board(rows, cols):
    board = []

    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(tree_game_lib.BOARD_EMPTY)
        board.append(row)

    return board


def play_game():
    trees = create_board(15, 30)

    for r in range(len(trees)):
        for c in range(len(trees[r])):
            if tree_game_lib.percent_chance(40):
                place_tent_and_tree(trees, r, c)

    tree_game_lib.print_board(trees)


play_game()
