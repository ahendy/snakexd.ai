from flask import Flask, request, jsonify
import json
import random
from snake import best, update_board
import datetime
from collections import namedtuple

app = Flask(__name__)
N = 15
moves = ["up", "down", "left", "right"]

GameState = namedtuple("game_state", ["me", "snakes", "food", "width", "height"])


@app.route("/start", methods=["POST"])
def start():
    # NOTE: 'request' contains the data which was sent to us about the Snake game
    # after every POST to our server 
    print(request.__dict__) 
    
    snake = {
        "color": "#123456",
        "name": "snak3",
        "taunt": "X D X D X D",
        "head_type": "pixel",
        "secondary_color": "#00000F"
    }

    return jsonify(snake)

@app.route("/move", methods=["POST"])
def move():
    t0 = datetime.datetime.now()
    data = json.loads(request.data)
    
    state = me, snakes, food, width, height, = get_params(data)
    board = update_board(state)


    response = {
        "move": best(state, board)
    }
    t1 = datetime.datetime.now()
    print("Time to run: ", (t1 - t0).total_seconds())
    return jsonify(response)

def get_params(data):
    print(data.keys())
    snakes = data['snakes']
    food = data['food']
    width = data['width']
    height = data['height']
    me = data['you']

    return GameState(me, snakes, food, width, height)




if __name__ == "__main__":
    app.run(port=8080, debug=True)


