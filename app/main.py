import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

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

    height = data['board']['height']
    width = data['board']['width']
    id = data['you']['id']
    health = data['you']['health']
    head = data['you']['body'][0]

    snakes = []
    for snake in data['board']['snakes']:
      for body in snake['body']:
        snakes.append(body)

    me = []
    for bod in data['you']['body']:
      me.append(bod)

    food = []
    for fo in data['board']['food']:
       food.append(fo)

    path = {'x':0, 'y':0}
    #right
    path['x'] = head['x']+1
    path['y'] = head['y']
    if (path in snakes or path['x'] > width-1 or path['x'] <0 or path['y']>height-1 or path['y'] <0) == False:
      direction = directions[3]
    #left
    path['x'] = head['x']-1
    path['y'] = head['y']
    if (path in snakes or path['x']>width-1 or path['x'] <0 or path['y']>height-1 or path['y'] <0) == False:
      direction = directions[1]
    #down
    path['x'] = head['x']
    path['y'] = head['y']+1
    if (path in snakes or path['x']>width-1 or path['x'] <0 or path['y']>height-1 or path['y'] <0) == False:
      direction = directions[2]
    #up
    path['x'] = head['x']
    path['y'] = head['y']-1
    if (path in snakes or path['x']>width-1 or path['x'] <0 or path['y']>height-1 or path['y'] <0) == False:
      direction = directions[0]

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
