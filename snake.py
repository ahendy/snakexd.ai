moves = 'north south east west'.split()
 
board = [[] for _ in N]
 
change = dict(
    north=(0, 1),
    south=(0, -1),
    east=(1, 0),
    west=(-1, 0))
 
def best(moves):
    return max(moves, key=lambda x: h(x))
 
def h(move):
    return sum(
        closest(i, j, snakes)
        for i in range(N)
        for j in range(N)
    )
 
def closest(x, y, snakes):
        me = snake[0]
 
        closest = min(snakes,
            key=lambda snake:
            dist(snake,
                 (x, y)))
 
        return me == closest
 
def dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])
