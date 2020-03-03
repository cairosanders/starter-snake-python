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

    height = data['board']['height']
    width = data['board']['width']
    grid = [[0 for col in xrange(height)] for row in xrange(width)]
    id = data['you']['id']
    health = data['you']['health']

    for snake in data['snakes']:
        if snake['id'] == id:
            grid[coord[0]][coord[1]] = ME
        for body in snake['body']:
            grid[coord[0]][coord[1]] = SNAKE

    for food in data['board']['food']:
        grid[food[0]][food[1]] = FOOD """

    direction = directions[2]

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
