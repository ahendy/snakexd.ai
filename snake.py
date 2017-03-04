
moves = ["up", "down", "left", "right"]
 
change = dict(
    north=(0, -1),
    south=(0, 1),
    east=(1, 0),
    west=(-1, 0))

SAFE = set(["0", "F"])

def safe(board, state, x, y):
    return 0 <= y < state.height and 0 <= x < state.height and board[y][x] in SAFE

def best(state, board):
    return max(moves, key=lambda x: h(state, board))
 
def h(state, board):
    return sum(
        closest(i, j, state)
        for i in range(state.width)
        for j in range(state.height)
        if safe(board, state, i, j)
    )
 
def closest(x, y, state):
        me = state.me
        snakes = state.snakes

        closest = min(snakes,
            key=lambda snake:
            dist(
                snake['coords'][0], # account for entire snake bodies? instead of just head
                (x, y)
            )
        )
 
        return me == closest 

def update_board(state):
    snakes = state.snakes
    food = state.food
    width = state.width
    height = state.height

    board = [['0']*width for _ in range(height)]
    for snake in snakes:
        for (x, y) in snake['coords']:
            print x, y
            board[y][x] = snake['id']
    
    for (x, y) in food:
        board[y][x] = "F"

    return board

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
