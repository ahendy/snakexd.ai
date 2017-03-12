from collections import namedtuple
import copy

GameState = namedtuple("game_state", ["me", "snakes", "food", "width", "height", "head"])

moves = ["up", "down", "left", "right"]
POSITION_UNSAFE_PENALTY = -100
change = dict(
        up=(0, -1),
        down=(0, 1),
        left=(-1, 0),
        right=(1, 0)
)

SAFE = set(["0", "F"])

def best(state, board, depth):
    """returns best move in moves such that h function is optimized"""
    head = head_x, head_y = get_head(state.me)
    safe_move = list(moves) # make new list as to not ruin state
    safe_move = [
        move for move in safe_move if safe(
            board, state, 
            *add_points(head, get_2d_mapping(move))
        )
    ]
    # TODO: account for all snakes
    return max(safe_move, key=lambda move: h(state, board, move, depth))

def apply_move(state, snake, move):
    """update state determined by snake and move applied to it"""
    state_copy = GameState(**state._asdict()) # copy 
    # state_copy  = state
    head = get_head(state.me)
    new_head = add_points(head, move)
    snake['coords'].pop() # pop tail
    snake['coords'] = [new_head] + snake['coords'] # Update snake head

    for s in state_copy.snakes:
        if s['id'] == snake['id']:
            s['coords'] = snake['coords'] # update state of snake
    
    if snake['id'] == state.me['id']: # if snake is me update me aswell (redundant?)
        snate.me = snake

    return state_copy, update_board(state_copy)


def h(state, board, move, depth):
    """
    Chose the move which maximizes 
    the number of spaces the snake is closest to
    """
    head = get_head(state.me)
    move = change[move]
    new_head = add_points(head, move)

    if safe(board, state, *head): # check that space is a safe space
        state, board = apply_move(state, state.me, move)
        return sum(
            is_closest((i, j), state, board, depth)
            for i in range(state.width)
            for j in range(state.height)
            if safe(board, state, i, j)
        )
    
    else:
        """unsafe position heuristic updator"""
        return POSITION_UNSAFE_PENALTY

def is_closest(curr_pt, state, board, depth):
        """find the closest snake on the board to position x, y"""
        me = state.me['id']
        snakes = state.snakes

        closest = min(snakes,
            key=lambda snake: # chose closest snake
                dist(
                    get_head(snake), # account for entire snake bodies? instead of just head?
                    curr_pt
                )
        )   

        return (me == closest['id']) * score(board, state, closest, depth)

def score(board, state, closest, depth):
    """recursively score a snake heads position altered by state of board. Emphasize food collection"""
    x, y = head = get_head(closest)
    HUNGER = 100 - closest['health_points']
    CONTAINS_FOOD = board[y][x] == 'F' # award a place if a food is contained 

    return (1 + (HUNGER**2) * (CONTAINS_FOOD)) + 0.5 * best(state, board, depth - 1) if depth >= 0 else 0

def update_board(state):
    """return matrix of board given snakes and food state"""
    snakes = state.snakes
    food = state.food
    width = state.width
    height = state.height

    board = [['0'] * width for _ in range(height)]
    for snake in snakes:
        for (x, y) in snake['coords']:
            board[y][x] = '2'#snake['id']
    
    for (x, y) in food:
        board[y][x] = "F"

    return board

def dist(p1, p2):
    """returns the manhattan distance between two points p1, p2 """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def printboard(board):
    for x in board:
        print x
    print "-" * len(board)

def safe(board, state, x, y):
    """returns True if provided board/state at (x,y) is considered a safe move"""
    return 0 <= y < state.height and 0 <= x < state.width and board[y][x] in SAFE

def get_2d_mapping(move):
    """map string to a move on a 2d matrix"""
    return change[move] 

def add_points(p1, p2):
    """return 2d space of p1+p2"""
    return (p1[0] + p2[0], p1[1], p2[1])

def get_head(snake):
    """return first coordinate of snake"""
    return snake['coords'][0]