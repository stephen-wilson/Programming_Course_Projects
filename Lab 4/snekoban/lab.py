# Snekoban Game

import json
from logging.handlers import BaseRotatingHandler
from os import terminal_size
import typing

# NO ADDITIONAL IMPORTS!


# GLOBAL VARIABLES
direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}

target_locations = {}
wall_locations = {}
board_size = ()

# Additional Helper Functions
def can_move_to(game, new_pos, new_comp_pos):
    # check if there is a wall or not
    # if new_pos not in game[3]:
    #     # check if there is a computer at that spot
    #     if new_pos in game[1]:
    #         # check if a computer isin the direction it is being pushed
    #         return new_comp_pos not in game[1] and new_comp_pos not in game[3]
    #     else:
    #         return True
    # else:
    #     return False
    
    if new_pos not in wall_locations:
        # check if there is a computer at that spot
        if new_pos in game[1]:
            # check if a computer isin the direction it is being pushed
            return new_comp_pos not in game[1] and new_comp_pos not in wall_locations
        else:
            return True
    else:
        return False

def find_token(state, token): 
    """
    Given a game state and token to find, goes through each row and column to see if a state
    is there, and if so, it adds it to a set.
    
    Returns a set of object location tuples where the given token string is on the board.
    """
    # use next(iter(set)) to get first element of set for player token
    objs_to_return = set()
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col]:
                # account for length 2 possibility
                for i in range(len(state[row][col])):
                    if state[row][col][i] == token:
                        objs_to_return.add((row, col))
            
    return objs_to_return

def find_player(state):
    # returns the element in the set which should just be the player
    return next(iter(find_token(state, "player")))

def find_computers(state):
    return find_token(state, "computer")
    

def move_player(state, action):
    """
    Moves the player based on the input action and moves the pushes the computer if the
    player runs into it, only if there is no computer or wall in the direction it is being pushed.
    
    Returns a new game with the same representation without modifying the original.
    """
    direction = direction_vector[action]
    # tuple + () copies the tuple to not change original
    # the below copy method speeds up runtime by ~ 4 seconds because the last 3 indices
    # aren't being copied over again when they are static anyway
    
    # copying every element to new set takes O(k) for k elements in the set
    # game = [state[0] + (), {computer_pos for computer_pos in state[1]}, state[2], state[3], state[4]]
    game = [state[0] + (), {computer_pos for computer_pos in state[1]}]
    new_pos = (game[0][0] + direction[0], game[0][1] + direction[1])
    new_comp_pos = (new_pos[0] + direction[0], new_pos[1] + direction[1])
    # can_move = True
    # # check if there is a wall or not
    # if new_pos not in game[3]:
    #     # check if there is a computer at that spot
    #     if new_pos in game[1]:
    #         new_comp_pos = (new_pos[0] + direction[0], new_pos[1] + direction[1])
    #         # check if computer in the direction it is being pushed
    #         if new_comp_pos not in game[1] and new_comp_pos not in game[3]:
    #             game[1].remove(new_pos)
    #             game[1].add(new_comp_pos)
    #         else:
    #             can_move = False
    # else:
    #     can_move = False
    
    # if can_move:
    #     game[0] = new_pos
    # stepped_game = state
        
        
    if can_move_to(game, new_pos, new_comp_pos):
        # stepped_game = tuple([new_pos, frozenset()])
        game[0] = new_pos
        if new_pos in game[1]:
            game[1].remove(new_pos)
            game[1].add(new_comp_pos)
        
    return game

def player_surroundings(state):
    pass


# -------------------------------


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    
    - wall locations and target locations are static. player and computer locations are dynamic.
    
    dictionary?: {"player": (p1,p2), "computers": (c1, c2), "targets": (t1,t2), "walls": (w1,w2)}
    list of sets?: [(1,2), {(c1,c2), (c3,c4)}, {(t1,t2), (t3,t4)}, {(w1,w2), (w3,w4)}] - YES!(?)
    
    {player, {computer locations tuples}}
    """
    # idx 0 = player, idx 1 = computers, idx 2 = targets, idx 3 = walls, idx 4 = size of board
    # game_rep = [find_player(level_description), find_computers(level_description), 
    #             find_token(level_description, "target"), find_token(level_description, "wall"),
    #             (len(level_description), len(level_description[0]))]
    
    game_rep = [find_player(level_description), find_computers(level_description)]
    
    # change value of the global variables
    global target_locations, wall_locations, board_size
    target_locations = find_token(level_description, "target")
    wall_locations = find_token(level_description, "wall")
    board_size = (len(level_description), len(level_description[0]))
    
    return game_rep


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    
    Victory condition: each target has a computer on top of it.
    """
    # if game[2]:
    #     for target in game[2]:
    #         if target not in game[1]:
    #             return False
    # else:
    #     return False
        
    # return True
    if target_locations:
        for target in target_locations:
            if target not in game[1]:
                return False
    else:
        return False
        
    return True
    


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    return move_player(game, direction)


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    # initial empty board
    board = [[[] for col in range(board_size[1])] for row in range(board_size[0]) ]
    # set each token to its respective position on the board
    # print(f"GAME[0]: {game[0]}")
    board[game[0][0]][game[0][1]].append("player")
    # for target in game[2]:
    #     board[target[0]][target[1]].append("target")
    # for computer in game[1]:
    #     board[computer[0]][computer[1]].append("computer")
    # for wall in game[3]:
    #     board[wall[0]][wall[1]].append("wall")
        
    for target in target_locations:
        board[target[0]][target[1]].append("target")
    for computer in game[1]:
        board[computer[0]][computer[1]].append("computer")
    for wall in wall_locations:
        board[wall[0]][wall[1]].append("wall")
    
    return board

def neighboring_states(last_game):
    """
    Neighboring function
    """
    neighboring = []
    # actions = ["up", "left", "down", "right"]
    for action in direction_vector:
        direction = direction_vector[action]
        # calculate new player direction if moved in direction of the action
        new_pos = (last_game[0][0][0] + direction[0], last_game[0][0][1] + direction[1])
        # direction of computer if pushed by player
        new_comp_pos = (new_pos[0] + direction[0], new_pos[1] + direction[1])
        if can_move_to(last_game[0], new_pos, new_comp_pos):
            # only need the game elements that change for the neighbors and for visited set
            # dynamic_game_elems = (game[0], game[1])
            # if len(game) > 2: 
                # neighboring.append(((game[0],frozenset(game[1]),frozenset(game[2]), frozenset(game[3]), game[4]),action))
            # casting takes O(n)
            # neighboring.append(((game[0],frozenset(game[1])),action))
            
            # format: (last_game, [])
            # actions_copy = last_game[1].copy()
            neighboring.append(((last_game[0][0], frozenset(last_game[0][1])),last_game[1] + (action, )))
            # else:
            #     neighboring.append((game, action))
            
    return neighboring

def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    
    Algorithm:
    Use breadth first search. If there are no targets, return None. Check surroundings;
    if there is a computer
    
    The "nodes" are game states paired with actions (or, edges are actions to get between game states).
    Visited set has actions
    
    Agenda has actions {left, right, up, down} based on if those are valid moves.
    "BFS" by taking actions and adding next possible actions to the agenda
    
    agenda = [right, up, down, left, right, down]
    
    "neighbors" are the next actions that can be taken
    
    game states should go in visited and when you are adding a state to visited, add the action to get
    there to a paths variable too
    
    agenda = [(current game state 1, possible action 1), (current game state 2, possible action 4)]
    
    """
    print(not find_token(dump_game(game), "target"))
    if not find_token(dump_game(game), "target"):
        return None
    if victory_check(game):
        return ()
    
    last_game_rep = (game, tuple())
    # agenda = neighboring_states(agenda, game)
    initial_neighbors = neighboring_states(last_game_rep)
    # print(initial_neighbors)
    agenda = [neighbor for neighbor in initial_neighbors]
    # print(agenda)
    visited = {neighbor for neighbor in initial_neighbors}
    while agenda:
        # print(agenda)
        current_path = agenda.pop(0)
        terminal_state = current_path
        # print(f'term state: {terminal_state}')
        # print(f'Terminal state 0: {terminal_state[0]}')
        # print(f'Term state 1: {terminal_state[1]}')
        
        # print(visited)
        # for the game states after the next action
        stepped_game = step_game(terminal_state[0], terminal_state[1][-1])
        if (stepped_game[0], frozenset(stepped_game[1])) not in visited:
            for neighbor in neighboring_states((stepped_game, terminal_state[1])):
                if neighbor[0] not in visited:
                    # new_path = current_path + (neighbor, )
                    # terminal_path_copy = terminal_state[1].copy()
                    # new_path = (neighbor[0], neighbor[1])
                    
                    if victory_check(neighbor[0]):
                        # return [node[1] for node in new_path if node != new_path[-1]]
                        return neighbor[1][:-1]
                    
                    agenda.append(neighbor)
        visited.add(neighbor[0])
    
    # current_action = agenda.pop(0)
    # current_game = move_player(game, current_action)
    # neighbors = []
    return None
    


if __name__ == "__main__":
#     level_description = [
#    [["wall"], ["wall"], ["wall"], ["wall"],     ["wall"],   ["wall"]],
#    [["wall"], [],       [],       ["target"],   ["wall"],   ["wall"]],
#    [["wall"], [],       [],       ["wall"],     ["player"], ["wall"]],
#    [["wall"], [],       [],       ["computer"], [],         ["wall"]],
#    [["wall"], [],       [],       [],           ["wall"],   ["wall"]],
#    [["wall"], ["wall"], ["wall"], ["wall"],     ["wall"],   ["wall"]]
# ]
    
#     [
#     [['wall'], ['wall'], ['wall'], ['wall'],        ['wall'], ['wall']], 
#     [['wall'], [],      [],         ['target'],     ['wall'], ['wall']], 
#     [['wall'], [],      [],         ['wall'],       ['player'], ['wall']], 
#     [['wall'], [],      [],         ['computer'],   [],       ['wall']], 
#     [['wall'], [],      [],         [],             ['wall'], ['wall']], 
#     [['wall'], ['wall'], ['wall'],  ['wall'],        ['wall'], ['wall']]
#     ]
    
#     [[['wall'], ['wall'], ['wall'], ['wall'],   ['wall'], ['wall']], 
#      [['wall'], [], [],     ['target'],     ['wall'], ['wall']], 
#      [['wall'], [], [],     ['wall'],       ['player'], ['wall']], 
#      [['wall'], [],         ['computer'],   [], [], ['wall']], 
#      [['wall'], [], [], [], ['wall'], ['wall']], 
#      [['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']]]
    
#     # copied set
#     [[['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']], 
#      [['wall'], [], [], ['target'], ['wall'], ['wall']], 
#      [['wall'], [], [], ['wall'], ['player'], ['wall']], 
#      [['wall'], [], [], ['computer'], [], ['wall']], 
#      [['wall'], [], [], [], ['wall'], ['wall']], 
#      [['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']]]
    
#     # step game
#     [[['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']], 
#      [['wall'], [], [], ['target'], ['wall'], ['wall']], 
#      [['wall'], [], [], ['wall'], [], ['wall']], 
#      [['wall'], [], ['computer'], ['player'], [], ['wall']], 
#      [['wall'], [], [], [], ['wall'], ['wall']], 
#      [['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']]]
    
#     # multi step games
#     [[['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']], 
#      [['wall'], [], [], ['target'], ['wall'], ['wall']], 
#      [['wall'], [], [], ['wall'], [], ['wall']], 
#      [['wall'], ['computer'], ['player'], [], [], ['wall']], 
#      [['wall'], [], [], [], ['wall'], ['wall']], 
#      [['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']]]

#     win_0_level = [
#   [["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"]],
#   [["wall"], [], [], [], [], ["wall"]],
#   [["wall"], [], ["wall"], ["player"], [], ["wall"]],
#   [["wall"], [], ["computer"], ["target", "computer"], [], ["wall"]],
#   [["wall"], [], ["target"], ["target", "computer"], [], ["wall"]],
#   [["wall"], [], [], [], [], ["wall"]],
#   [["wall"], ["wall"], ["wall"], ["wall"], ["wall"], ["wall"]]
# ]
    
#     # new dump rep
#     [[['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']], 
#      [['wall'], [], [], [], [], ['wall']], 
#      [['wall'], [], ['wall'], ['player'], [], ['wall']], 
#      [['wall'], [], ['computer'], ['target', 'computer'], [], ['wall']], 
#      [['wall'], [], ['target'], ['target', 'computer'], [], ['wall']], 
#      [['wall'], [], [], [], [], ['wall']], 
#      [['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']]]
    
#     # dump:
#     [[['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']], 
#      [['wall'], [], [], [], [], ['wall']], 
#      [['wall'], [], ['wall'], ['player'], [], ['wall']], 
#      [['wall'], [], ['computer'], ['target'], [], ['wall']], 
#      [['wall'], [], ['target'], ['target'], [], ['wall']], 
#      [['wall'], [], [], [], [], ['wall']], 
#      [['wall'], ['wall'], ['wall'], ['wall'], ['wall'], ['wall']]]
    
#     temp_game = new_game(win_0_level)
#     # step_game = step_game(step_game(step_game(step_game(temp_game, "down"), "left"), "left"),"up")
#     print(dump_game(temp_game))
    test_game = [
  [["wall"], ["wall"], ["wall"], ["wall"], [], []],
  [["wall"], [], ["target"], ["wall"], [], []],
  [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
  [["wall"], ["target", "computer"], ["player"], [], [], ["wall"]],
  [["wall"], [], [], ["computer"], [], ["wall"]],
  [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
  [["wall"], ["wall"], ["wall"], ["wall"], [], []]
]
    
    print(solve_puzzle(new_game(test_game)))