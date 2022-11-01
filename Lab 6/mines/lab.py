#!/usr/bin/env python3

from dataclasses import replace
from email.errors import NoBoundaryInMultipartDefect
from multiprocessing import allow_connection_pickling
import numbers
import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION

def num_neighbor_bombs(num_rows, num_cols, board, row_idx, col_idx):
    """
    Counts the number of bombs in the surroundings of a space on the board.
    
    Returns:
    int:num neighbor bombs
    """
    dimensions = (num_rows, num_cols)
    coord = (row_idx, col_idx)
    neighbors = neighbors_of(dimensions, coord)
    return neighbor_bombs_nd(neighbors, board)
    

def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    dimensions = (num_rows, num_cols)
    return new_game_nd(dimensions, bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    coord = (row, col)
    return dig_nd(game, coord)


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    # index over every element, if xray is true and the index at that location in hidden 
    # is also true, set it to '_', otherwise, add the original value. If 0 is the value, add ' '
    return render_nd(game, xray)


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    locations_2d = render_2d_locations(game, xray)
    game_rep_str = ''
    for row_idx in range(len(locations_2d)):
        for col_idx in range(len(locations_2d[row_idx])):
            game_rep_str += locations_2d[row_idx][col_idx]
        if row_idx is not len(locations_2d) - 1:
            game_rep_str += '\n'
            
    return game_rep_str


# N-D IMPLEMENTATION

# helper functions
def get_nd_value(nd_arr, coords):
    """
    Returns the value at the specified index by repeatedly indexing into it.
    """
    current_arr = nd_arr
    for coord in coords:
        if 0 <= coord < len(current_arr):
            current_arr = current_arr[coord]
        else:
            raise IndexError
    return current_arr # returns the value at the specified index

def replace_nd_value(nd_arr, coords, value):
    """
    Replaces current value at coords with new (param) value. 
    """
    # modifies original
    current_arr = nd_arr
    for coord in coords:
        if 0 <= coord < len(current_arr):
            # index into array until you get to the inner integers
            if isinstance(current_arr[coord], list):
                current_arr = current_arr[coord]
        else:
            raise IndexError
    current_arr[coords[-1]] = value
    # return nd_arr
    return None

def create_nd_arr(dimensions, value):
    """
    Recursively create nd array.
    """
    out = []
    # base case
    if not dimensions:
        return value
    else:
        for _ in range(dimensions[0]):
            out.append(create_nd_arr(dimensions[1:],value))
    return out

def game_state(game):
    """
    Determines the current game state.
    """
    bombs = 0
    hidden_squares = 0
    for coord in all_coordinates(game["dimensions"]):
        hidden_val = get_nd_value(game["hidden"], coord)
        if get_nd_value(game["board"], coord) == ".":
            if hidden_val == False:
                bombs += 1
        elif hidden_val == True:
            hidden_squares += 1
    
    if bombs != 0:
        return "defeat"
    elif hidden_squares == 0:
        return "victory"
    else:
        return "ongoing"
    


def neighbors_of(dimensions, coords):
    """
    Returns the neighbords of the given coordinate.
    Check all neighbors whenever you dig.
    Invalid neighbors included. (?)
    """
    
    
    neighbors = []
    out = []
    # base case
    if len(coords) == 1:
        return [((coords[0] + i), ) for i in range(-1,2) 
                if (coords[-1] + i >= 0 and coords[-1] + i < dimensions[-1])]
    # recursive case, back to front
    else:
        neighbors = neighbors_of(dimensions[:-1], coords[:-1])
        # offsets = []
        for i in range(-1,2):
            if coords[-1] + i >= 0 and coords[-1] + i < dimensions[-1]:
                for neighbor in neighbors:
                    out.append(neighbor + ((coords[-1] + i),))
    # remove all the ones less than 0 or greater than the coord
    # remove before returning
    
    return out

def all_coordinates(dimensions):
    """
    Returns all possible coordinates of the board using recursion.
    """
    all_coords = []
    out = []
    # base case
    if len(dimensions) == 1:
        return [(i,) for i in range(dimensions[0])]
    # recursive case, go from back to front
    else:
        all_coords = all_coordinates(dimensions[:-1])
        for i in range(dimensions[-1]):
            for coord in all_coords:
                out.append(coord + (i,))
    return out 

def neighbor_bombs_nd(neighbors, board):
    """
    Count the number of bombs that are neighbors.
    """
    num_bombs = 0
    for neighbor in neighbors:
        if get_nd_value(board, neighbor) == '.':
            num_bombs += 1
    return num_bombs
        
########



def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    
    {'dimensions': (), 'board': [], 'hidden': [], 'state': 'ongoing'}
    """
    board = create_nd_arr(dimensions,0)
    hidden = create_nd_arr(dimensions, True)
    possible_coords = all_coordinates(dimensions)
    
    # set bombs vals
    for bomb in bombs:
        replace_nd_value(board, bomb, '.')
    
    bombs_set = set(bombs)
    
    # set values of the spots
    for coord in possible_coords:
        neighbors = neighbors_of(dimensions, coord)
        if coord not in bombs_set:
            replace_nd_value(board, coord, neighbor_bombs_nd(neighbors,board))
           
    return  {'dimensions': dimensions, 'board': board, 'hidden': hidden, 'state': 'ongoing'}


def dig_nd(game, coordinates, first_rec_call = True):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat
    """
    if game["state"] == "defeat" or game["state"] == "victory":
        game["state"] = game["state"]  # keep the state the same
        return 0

    board_value = get_nd_value(game["board"], coordinates)
    hidden_value = get_nd_value(game["hidden"], coordinates)
    neighbors = neighbors_of(game["dimensions"], coordinates)

    if board_value == ".":
        replace_nd_value(game["hidden"], coordinates, False)
        game["state"] = "defeat"
        return 1
    
    # unhide current tile
    revealed = 0
    if hidden_value != False:
        replace_nd_value(game["hidden"], coordinates, False)
        revealed = 1
    else:
        return 0
    
    if board_value == 0:
        for neighbor in neighbors:
            if get_nd_value(game["board"], neighbor) != ".":
                if get_nd_value(game["hidden"], neighbor) == True:
                    revealed += dig_nd(game, neighbor, first_rec_call=False)
    
    if first_rec_call:
        if game_state(game) == "ongoing":
            game["state"] = "ongoing"
            return revealed
        else:
            game["state"] = "victory"
            return revealed
    return revealed
    
    

def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
     
     orig_board = game['board']
    render_board = []
    
    for row_idx in range(len(orig_board)):
        row = orig_board[row_idx]
        row_to_add = []
        for col_idx in range(len(row)):
            if not xray and game['hidden'][row_idx][col_idx]:
                row_to_add.append('_')
            else:
                if row[col_idx] == 0:
                    row_to_add.append(' ')
                else:
                    row_to_add.append(str(row[col_idx]))
        render_board.append(row_to_add)
    return render_board
    """
    render_board = create_nd_arr(game['dimensions'], '_')
    
    all_coords = all_coordinates(game['dimensions'])
    
    for coord in all_coords:
        if xray or not get_nd_value(game['hidden'], coord):
            value = get_nd_value(game['board'], coord)
            if value == 0:
                replace_nd_value(render_board, coord, ' ')
            else:
                replace_nd_value(render_board, coord, str(value))
        

    return render_board



if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    # print(all_coordinates((2,4,2)))
    # print(neighbors_of((10,20),(9,19)))
    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    #doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
