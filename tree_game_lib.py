import random
import msvcrt

BOARD_TENT = "^"
BOARD_TREE = "Ŷ"
BOARD_EMPTY = " "
BOARD_OUT_OF_BOUNDS = "!"
BOARD_EMPTY_GUESS = "~"
BOARD_BORDER_COL = "│"
BOARD_BORDER_ROW = "-"


class OutOfRange(BaseException):
    pass


def validate(board, row=None, col=None):
    """Validate that row and col are within the board boundaries.

    Verify that row and col are both within the boundaries of the
    board. If they are not, throw an exception.

    Args:
        board - The game board
        row   - The number of a row in the board
        col   - The number of a col in the board

    Returns:
        none

    Throws:
        OutOfRange - Either row or col are outside of tbe boundaries
        of the board.
    """
    if row is None and col is None:
        raise OutOfRange("Either row or col must be set")

    if row:
        if row > len(board) - 1 or row < 0:
            raise OutOfRange("row of %d is outside range 0..%d" % (row, len(board) - 1))

    if col:
        if col > len(board[0]) - 1 or col < 0:
            raise OutOfRange("col of %d is outside range 0..%d" % (col, len(board[0]) - 1))


def get(board, row, col):
    """A boundary-safe way to inspect board contents.

    If you try to access outside of the boundary of the board
    Python will throw a bounds exception. But, the code you
    have to write to check that you are within the bounds is
    really messy. Instead of making each access to the board
    check first whether it is within bounds, allow accesses
    outside of the board, but instead of crashing return an
    indicator that you are out of bounds.

    Args:
        board - The game board
        row   - Any integer
        col   - Any integer

    Returns:
        If row,col is inside the board:
            The contents of board[row][col]
        If row,col is outside the board:
            BOARD_OUT_OF_RANGE
    """
    # The coordinates are out of bounds
    try:
        validate(board, row, col)
    except OutOfRange:
        return BOARD_OUT_OF_BOUNDS

    return board[row][col]


def set(board, row, col, val):
    """A boundary-safe way to change board contents.

    If you try to access outside of the boundary of the board
    Python will throw a bounds exception. But, the code you
    have to write to check that you are within the bounds is
    really messy. Instead of making each access to the board
    check first whether it is within bounds, allow accesses
    outside of the board, but instead of crashing return an
    indicator that you are out of bounds.

    Args:
        board - The game board
        row   - Any integer
        col   - Any integer
        val   - The value to set

    Returns:
        none
    """
    # The coordinates are out of bounds
    try:
        validate(board, row, col)
    except OutOfRange:
        return

    board[row][col] = val


def percent_chance(percent):
    """Given a probability percent, roll a die and see whether an event happened.

    Given the probability that something will happen, roll a 100-sided
    die and determine whether it did happen or not. For instance, if
    the probability it will rain is 30% (percent=30) roll a die. If the
    result is 30 or less then it did rain.

    Args:
        percent - The percent chance the event will happen.
            0   = It will never happen
            100 = It will always happen

    Returns:
        True  - The event happened
        False - The event did not happen
    """
    return random.randint(1, 100) <= percent


def is_tent(board, row, col):
    """Is this value a tent?

    Args:
        c - The character to examine

    Returns:
        True  - This character is a tent
        False - This character is not a tent
    """
    return get(board, row, col) == BOARD_TENT


def count_tents(board, row=None, col=None, match=BOARD_TENT):
    """Count the number of tents in a given row or col.

    Given a row or a col, count the number of tents
    that are present. Only one (row or col) can be
    asked for at a time.

    Args:
        board - The board
        row   - If set, the index of the row to count
        col   - If set, the index of the col to count

    Returns:
        int - The number of tents in that row or col

    Throws:
        OutOfRange - Either row or col are outside of tbe boundaries
        of the board.
    """
    validate(board, row=row, col=col)

    tents = 0

    if row is not None:
        for c in range(len(board[row])):
            if get(board, row, c) == match:
                tents += 1
        return tents

    if col is not None:
        for r in range(len(board)):
            if get(board, r, col) == match:
                tents += 1
        return tents


def print_board(board, guess=None, cursor=None):
    """Print the board.

    Print the board, including the tent counts along
    the side and top. If only the board is passed in,
    just print the board, including showing where the
    tents are. If the player's guessing board is also
    passed in, then print the board as the player has
    completed it so far, but still also include the
    tent counts from the actual board.

    Args:
        board - The board
        guess - The player's guesses

    Returns:
        none
    """
    # If we are not using a cursor, move it off the board
    cursor = cursor or [-1, -1]

    # Print the number of tents in each column
    record = " "
    for col in range(len(board[0])):
        record += ("%s" % count_tents(board, col=col))
    print(record)

    # Print the board's top border
    border_row = " "
    for col in range(len(board[0])):
        border_row += BOARD_BORDER_ROW
    print(border_row)

    # Print each row, with borders and tent count
    for row in range(len(board)):
        record = BOARD_BORDER_COL
        for col in range(len(board[row])):
            if row == cursor[0] and col == cursor[1]:
                record += chr(27) + "[7m"
            if guess:
                record += guess[row][col]
            else:
                record += board[row][col]
            if row == cursor[0] and col == cursor[1]:
                record += chr(27) + "[0m"
        record += BOARD_BORDER_COL + " " + ("%s" % count_tents(board, row=row))
        print(record)

    # Print the board's bottom border
    print(border_row)


def can_place_tent(board, row, col):
    """Determine whether it is not illegal to place a tent at board[row][col].

    Look at the board state to see whether a tent would be illegal
    if placed at board[row][col]. We don't know if it would be LEGAL,
    because that would involve way more analysis of tree placement,
    so we leave that part to the caller to figure out.

    Args:
        board - The game board
        row   - The row of the square on the board
        col   - The col of the square on the board

    Returns:
        True  - It is not illegal to place a tent at row,col
        False - It is illegal to place a tent at row,col
    """
    # The coordinates are out of bounds
    try:
        validate(board, row, col)
    except OutOfRange:
        return False

    # There is already something in this square
    if board[row][col] != BOARD_EMPTY:
        return False

    # There is a tent in this or any adjacent square
    for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            if is_tent(board, row+r, col+c):
                return False

    # No illegal cases found
    return True


def place_tree_and_tent(board, row, col):
    """Put a tree and its tent on the board.

    Given a coordinate on the board, find an adjacent square that can
    legally have a tent and put a tent there. If there are multiple
    legal adjacent squares, then select one at random. If there are
    none, do not place a tent nor a tree.

    Args:
        board - The game board
        row   - The index of a row on the board
        col   - The index of a col on the board

    Returns:
        none
    """
    validate(board, row, col)

    if board[row][col] != BOARD_EMPTY:
        return

    # Find all of the adjacent squares that would allow a tent
    choices = []
    for r, c in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
        if can_place_tent(board, row+r, col+c):
            choices.append([row+r, col+c])

    if len(choices) <= 0:
        return

    # Randomly select one of the choices
    choice = random.randint(0, len(choices)-1)
    r = choices[choice][0]
    c = choices[choice][1]
    board[r][c] = BOARD_TENT
    board[row][col] = BOARD_TREE


def create_board(rows, cols, density=30):
    """Create and populate a new board.

    A board is a list of lists of the form:
    [
        [ tree, empty, tent ],
        [ tent, empty, tree ]
    ]

    Args:
        rows    - The number of rows to put in the board
        cols    - The number of cols to put in the board
        density - The density of trees as a percentage (0-100)

    Returns:
        A new board (a list of lists) consisting of trees,
        their associated tents, and the remaining squares
        marked as empty.
    """
    board = []
    for r in range(rows):
        board.append([BOARD_EMPTY] * cols)

    for row in range(len(board)):
        for col in range(len(board[row])):
            if percent_chance(density):
                place_tree_and_tent(board, row, col)

    return board


def create_guess_board(board):
    """Make a copy of a board, but blank out the tents.

    The initially generated board has the tents on it. The player
    will want a scratch board they can make their guesses in. This
    scratch board will need to have the tents removed so the
    player can guess where they are.

    Args:
        board - The board to copy

    Returns:
        A copy of the board, but with any tents replaced
        with empty.
    """
    guess = []
    for row in range(len(board)):
        guess.append([BOARD_EMPTY] * len(board[row]))

    for row in range(len(guess)):
        for col in range(len(guess[row])):
            if board[row][col] == BOARD_TENT:
                guess[row][col] = BOARD_EMPTY
            else:
                guess[row][col] = board[row][col]

    return guess


def solved(board, guess):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if get(board, row, col) == BOARD_TENT:
                if get(guess, row, col) != BOARD_TENT:
                    return False
            else:
                if get(guess, row, col) == BOARD_TENT:
                    return False

    return True


def fill_empty(board, guess):
    # If the row has all its tents, the remaining squares must be empty
    for row in range(len(guess)):
        need = count_tents(board, row=row)
        have = count_tents(guess, row=row)
        if need == have:
            for col in range(len(guess[row])):
                if guess[row][col] == BOARD_EMPTY:
                    set(guess, row, col, BOARD_EMPTY_GUESS)

    # If the col has all its tents, the remaining squares must be empty
    for col in range(len(guess[0])):
        need = count_tents(board, col=col)
        have = count_tents(guess, col=col)
        if need == have:
            for row in range(len(guess)):
                if guess[row][col] == BOARD_EMPTY:
                    set(guess, row, col, BOARD_EMPTY_GUESS)

    # A square that has no trees adjacent to it cannot have a tent
    for row in range(len(guess)):
        for col in range(len(guess[row])):
            if get(guess, row, col) == BOARD_EMPTY:
                tree = False
                for adjacent in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                    if get(guess, row+adjacent[0], col+adjacent[1]) == BOARD_TREE:
                        tree = True
                if not tree:
                    set(guess, row, col, BOARD_EMPTY_GUESS)


def solver(board, guess):
    modified = True

    while modified:
        modified = False

        for row in range(len(guess)):
            tents = count_tents(board, row=row)
            empty = count_tents(guess, row=row, match=BOARD_EMPTY)
            have = count_tents(guess, row=row)
            if tents == have + empty:
                for col in range(len(guess[row])):
                    if guess[row][col] == BOARD_EMPTY:
                        set(guess, row, col, BOARD_TENT)
                        modified = True

        for col in range(len(guess[0])):
            tents = count_tents(board, col=col)
            empty = count_tents(guess, col=col, match=BOARD_EMPTY)
            have = count_tents(guess, col=col)
            if tents == have + empty:
                for row in range(len(guess)):
                    if guess[row][col] == BOARD_EMPTY:
                        set(guess, row, col, BOARD_TENT)
                        modified = True

        # A tree that has no tents around it and only one empty adjacent square
        for row in range(len(guess)):
            for col in range(len(guess[row])):
                if get(guess, row, col) == BOARD_TREE:
                    empty = []
                    tent = False
                    for adjacent in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                        if get(guess, row+adjacent[0], col+adjacent[1]) == BOARD_EMPTY:
                            empty.append(adjacent)
                        if get(guess, row + adjacent[0], col + adjacent[1]) == BOARD_TENT:
                            tent = True
                    if len(empty) == 1 and not tent:
                        adjacent = empty[0]
                        if get(guess, row + adjacent[0], col + adjacent[1]) == BOARD_EMPTY:
                            set(guess, row + adjacent[0], col + adjacent[1], BOARD_TENT)
                            modified = True

        # A square that has a tent cannot have tents around it
        for row in range(len(guess)):
            for col in range(len(guess[row])):
                if get(guess, row, col) == BOARD_TENT:
                    for r in [-1, 0, 1]:
                        for c in [-1, 0, 1]:
                            if get(guess, row+r, col+c) == BOARD_EMPTY:
                                set(guess, row+r, col+c, BOARD_EMPTY_GUESS)
                                modified = True

        # If a tent has only one tree near it, then it must
        # satisfy that tree. If that tree has open spaces
        # around it that do not touch other trees, then we
        # know those open spaces cannot have tents.
        for row in range(len(guess)):
            for col in range(len(guess[row])):
                if get(guess, row, col) == BOARD_TENT:
                    trees = []
                    for adjacent in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                        if get(guess, row+adjacent[0], col+adjacent[1]) == BOARD_TREE:
                            trees.append([row+adjacent[0], col+adjacent[1]])
                    # If a tent has only one tree near it then it must satisfy that tree.
                    if len(trees) == 1:
                        r = trees[0][0]
                        c = trees[0][1]
                        for adjacent in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                            if get(guess, r + adjacent[0], c + adjacent[1]) == BOARD_EMPTY:
                                # If that tree has open spaces around it ...
                                count = 0
                                empty_r = r + adjacent[0]
                                empty_c = c + adjacent[1]
                                for adjacent in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                                    if get(guess, empty_r + adjacent[0], empty_c + adjacent[1]) == BOARD_TREE:
                                        count += 1
                                # ... that do not touch other trees
                                if count == 1:
                                    set(guess, empty_r, empty_c, BOARD_EMPTY_GUESS)
                                    modified = True


def play():
    """Play the game. Let the user try to solve it.

    Returns:
        none
    """
    count = 0
    while True:
        count += 1
        board = create_board(6, 6, density=40)
        guess = create_guess_board(board)
        fill_empty(board, guess)
        print('Attempting to solve (%d) ...' % count)
        solver(board, guess)
        if solved(board, guess):
            guess = create_guess_board(board)
            fill_empty(board, guess)
            break

    cursor = [0, 0]

    while True:
        print()
        print_board(board, guess, cursor=cursor)
        if solved(board, guess):
            print('\nYou solved it. Great work!')
            break
        # stuff = input('Your turn [1-9, ~, ^, s, ?, h, q]: ')
        # command = stuff.split()
        print('Your turn [1-9, ~, ^, s, ?, h, q]: ')
        stuff = msvcrt.getch()
        print('stuff = /%s/' % stuff)
        command = stuff.split()
        if len(command) == 0:
            continue
        if command[0] == 'q':
            break
        elif command[0] == 'h':
            print_board(board, cursor=cursor)
        elif command[0] == 's':
            solver(board, guess)
        elif command[0] == '?':
            if board[cursor[0]][cursor[1]] == BOARD_TENT:
                set(guess, cursor[0], cursor[1], BOARD_TENT)
            if board[cursor[0]][cursor[1]] == BOARD_EMPTY:
                set(guess, cursor[0], cursor[1], BOARD_EMPTY_GUESS)
        elif command[0] in ['~', '^']:
            if get(guess, cursor[0], cursor[1]) == BOARD_TREE:
                print('Please do not cut down the trees!')
            else:
                set(guess, cursor[0], cursor[1], command[0])
        elif command[0] in ['1', '2', '3', '4', '6', '7', '8', '9']:
            dir = int(command[0])
            adjacent = [
                [0, 0],    #
                [1, -1],   # 1
                [1, 0],    # 2
                [1, 1],    # 3
                [0, -1],   # 4
                [0, 0],    #
                [0, 1],    # 6
                [-1, -1],  # 7
                [-1, 0],   # 8
                [-1, 1]    # 9
            ]
            cursor[0] += adjacent[dir][0]
            cursor[1] += adjacent[dir][1]
            if cursor[0] < 0:
                cursor[0] = len(board) - 1
            if cursor[0] >= len(board):
                cursor[0] = 0
            if cursor[1] < 0:
                cursor[1] = len(board[0]) - 1
            if cursor[1] >= len(board[0]):
                cursor[1] = 0
        else:
            print("""
Please type one of:
    # - Move the cursor in that direction
    ~ - Place an 'empty' marker at the current square
    ^ - Place a 'tent' marker at the current square
    h - Hint
    q - Quit
""")

    print_board(board)
