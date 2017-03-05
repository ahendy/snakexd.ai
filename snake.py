from collections import namedtuple
import copy

GameState = namedtuple("game_state", ["me", "snakes", "food", "width", "height", "head"])


moves = ["up", "down", "left", "right"]
 
change = dict(
    up=(0, -1),
    down=(0, 1),
    left=(-1, 0),
    right=(1, 0)
)

SAFE = set(["0", "F"])

def safe(board, state, x, y):
    return 0 <= y < state.height and 0 <= x < state.width and board[y][x] in SAFE

def best(state, board, depth):
    safe_move = copy.deepcopy(moves)
    safe_move = [move for move in safe_move
                if safe(board, state, state.me['coords'][0][0]+change[move][0], state.me['coords'][0][1]+ change[move][1])]

    return max(safe_move, key=lambda move: h(state, board, move, depth))

def apply_move(state, snake, move):
    state2 = GameState(**state._asdict())
    state2 = state
    y1, x1 = head = snake['coords'][0]
    y, x = move
    snake['coords'] = [(y1+y, x1+x)] + snake['coords'][:-1]

    for s in state2.snakes:
        if s['id'] == snake['id']:
            s['coords'] = snake['coords']
    
    return state2, update_board(state2)

def printboard(board):
    for x in board:
        print x
    print ""

def h(state, board, move, depth):
    x1, y1 = head = state.me['coords'][0]
    x, y = change[move]
    head = (x1+x, y1+y)

    if safe(board, state, head[0], head[1]):
        state, board = apply_move(state, state.me, change[move])
        # printboard(board)
        return sum(
            closest(i, j, state, board, depth)
            for i in range(state.width)
                for j in range(state.height)
                    if safe(board, state, i, j)
        )
    
    else:

        return -5000

def closest(x, y, state, board, depth):
        me = state.me['id']
        snakes = state.snakes

        closest = min(snakes,
            key=lambda snake:
            dist(
                snake['coords'][0], # account for entire snake bodies? instead of just head
                (x, y)
            )
        )   
        x, y = closest['coords'][0]
        return (me == closest['id']) * (1 + 45*(101-closest['health_points']) * (board[y][x] == 'F') + 0.5*(best(state, board, depth-1) if depth <= 0 else 0))

def update_board(state):
    snakes = state.snakes
    food = state.food
    width = state.width
    height = state.height

    board = [['0']*width for _ in range(height)]
    for snake in snakes:
        for (x, y) in snake['coords']:
            board[y][x] = '2'#snake['id']
    
    for (x, y) in food:
        board[y][x] = "F"

    return board

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
