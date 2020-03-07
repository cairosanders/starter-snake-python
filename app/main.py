import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
SNAKE = 8
WALL = 9
FOOD = -1
ME = 1

directions = ['up', 'left', 'down', 'right']

def min_direction(grid,x,y):
    #up
    right = grid[x][y+1]
    left = grid[x-1][y-1]
    up = grid[x-1][y]
    down = grid[x+1][y]
    direct = [up,down,left,right]
    mindirect = min(direct)
    print(direct)
    if mindirect == up:
      return directions[0]
    elif mindirect == left:
      return directions[1]
    elif mindirect == down:
      return directions[2]
    else:
      return directions[3]

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

    height = data['board']['height']
    width = data['board']['width']
    grid = [[0 for col in range(height)] for row in range(width)]
    id = data['you']['id']
    health = data['you']['health']
    head = data['you']['body'][0]

    for snake in data['board']['snakes']:
        for coord in snake['body']:
            grid[coord['x']][coord['y']] = SNAKE

    for coord in data['you']['body']:
        grid[coord['x']][coord['y']] = ME

    for food in data['board']['food']:
        grid[food['x']][food['y']] = FOOD

    for space in range(width):
        grid[0][space] = WALL
        grid[height-1][space] = WALL

    for space in range(height):
        grid[space][0] = WALL
        grid[space][width-1] = WALL

    direction = min_direction(grid, head['x'], head['y']) 
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
