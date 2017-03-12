# snakexd.ai

## the algorithm

The simple heuristic was: chose the move that makes my snake enter the space that makes me closest to the most free spaces.

So for each available/safe space I do a search, updating state of the board and graph of the snake who is being moved at that call. And then calculating a score based off how many spaces the snake is closest to. This works well for moving around and entering spaces that are not populated/covering a lot of area - but - this doesn't translate well for collecting food and the snake would onky survive based off luck. There is a couple options my partner and I thought of.

1. Keep track of HP and when below a certain threshhold eg. 30/100 or some math based off mean hp and then when that happens kick into a different state that would bfs to the closest food that wasnt closest to any other snakes. This works but would add an annoying ```if needs_food(snake) then food_search else normal_search()```. Which means that we were basically stuck with a bfs that couldn't be tuned later. Plus we really just wanted a declaritive AI rather than procedural. So instead we:

2. Account for food in the heuristic search using a weight of ```alpha*(100-snake.hp)**2```. This makes it so that in the recursive call paths that could lead to a food spot would return a hearty heuristic whenever the snake was getting hungry. Of course this was tuned in the recursive call by using the alpha parameter to make sure that we were staying in a simlar domain to counting a 15x15 board. Using the square allows us to REALLY want to reward food when hungry and tuning alpha allows us not to worry so much about food when not hungry and allow for a possible better path to open up.


## moving forward

Next year it would be super awesome to have a complete ```Alpha-Beta``` pruning or even just ```Minimax``` for making a search assuming others are making optimal moves. This would require a calculation of ```best(moves)``` and updating of state for every snake at every depth. This could be quite expensive in the early game (more open moves and more snakes alive => deeper search tree) and would be pretty much useless. We'd have to tune recursive depth based off of snake length. A heuristic such as ```log(len(longest_snake))``` could work to catch trapping of a snake within a 1xN Nx1 space and could probably be proven but not tonight (for now just visualize number of spaces needed to enter a dangerous spot and stay alive; this is recursive depth needed).
 
Flood fill enemy snakes to use a weighting or inverse weighting in the score function. Calculate path which provides the least area filled positions rather than just counting tiles (weight kinda like a minesweeper game).

Make a snake that attacks other snakes in a 1v1 position. In a 1v1 it should be (in theory) easy to deterministicly take advantage of the other snake given you have adequate length. This involves forcing the snake into a corner by diagonalizing (and if the have enough length to beat you to the corner and turn, diaganolize the the next closest corner again (and repeat till win).

## interesting fact

Our snake heuristic resulted in the snake learning to chase it's own tail. We thought that was quite an interesting interaction that was probably hard coded/proceduralized but could be covered within a mathematical function!

## Howto

1. Install Python & pip https://www.python.org/downloads/
 
 
 (optional but recommended)
    a. Install virtualenvwrapper https://virtualenvwrapper.readthedocs.io/en/latest/install.html 
    
    b. "mkvirtualenv snake" or (python3) "mkvirtualenv --python=which python3 snake" 
    
    c. "workon snake"

2. cd to this directory (snakexd.ai) and "pip install -r requirements.txt"

3. Run python snake.py (python2.7) or python3 snake.py (python 3.5)

4. Make the Snake a bit smarter!
