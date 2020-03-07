import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
SNAKE = 10
WALL = 10
FOOD = -10
ME = 1
directions = ['up', 'left', 'down', 'right']

def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]

    if dx == 1:
        return 'east'
    elif dx == -1:
        return 'west'
    elif dy == -1:
        return 'north'
    elif dy == 1:
        return 'south'

def one_move(square, direction):
    '''
    takes in a square and a direction and returns the square one step in that direction
    '''
    newSquare = {"x": 0, "y":0}
    if direction == "up":
        newSquare["x"] = square["x"]
        newSquare["y"] = square["y"] - 1
    elif direction == "down":
        newSquare["x"] = square["x"]
        newSquare["y"] = square["y"] + 1
    elif direction == "left":
        newSquare["x"] = square["x"] - 1
        newSquare["y"] = square["y"]
    elif direction == "right":
        newSquare["x"] = square["x"] + 1
        newSquare["y"] = square["y"]
    return newSquare

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#FFBFEA"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """

    height = data['board']['height']
    width = data['board']['width']
    grid = [[0 for col in xrange(height)] for row in xrange(width)]
    id = data['you']['id']
    health = data['you']['health']
    head = data['you']['body'][0]
    for snake in data['board']['snakes']:
        for coord in snek['body']:
            grid[coord[0]][coord[1]] = SNAKE

    for coord in data['you']['body']:
            grid[coord[0]][coord[1]] = ME

    for food in data['board']['food']:
        grid[food[0]][food[1]] = FOOD

    for space in range(width):
        grid[0][space] = WALL
        grid[height][space] = WALL

    for space in range(height):
        grid[space][0] = WALL
        grid[width][space] = WALL


    for direct in (directions):
        if one_move(head, direct) == FOOD:
            direction = directions[direct]
        elif one_move(head, direct) != SNAKE:
            direction = directions[direct]
        else:
            continue

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
