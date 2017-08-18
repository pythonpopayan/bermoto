"""
handlers for transactional messaging service
"""
import json

# tornado imports
from tornado.queues import Queue
from tornado import websocket, gen, web

#local imports
from settings import DEBUG


#===============================================================================
# WEBSOCKETS SERVER
#===============================================================================


class messaging_server(web.Application):
    """listener application class"""
    def __init__(self, q):
        """listener builder method"""
        #define petition handlers to use
        handlers = [
            (r'/channel', channelHandler, dict(q=q)),
            (r'/mirror', mirrorHandler),
        ]

        web.Application.__init__(self, handlers)

#===============================================================================
# TESTING HANDLERS
#===============================================================================


class mirrorHandler(websocket.WebSocketHandler):
    """return to the sender the same message they sent"""
    verbose = DEBUG

    def open(self):
        """defines the websocket open method"""
        pass

    @gen.coroutine
    def on_message(self, message):
        """mirror income data"""
        yield self.write_message(message)

    def on_close(self):
        """defines the websocket close method"""
        pass


class channelHandler(websocket.WebSocketHandler):
    """class that handles app websockets communication"""
    verbose = DEBUG

    def initialize(self, q):
        """initialize vigilante handler"""
        self.q = q
        self.service_functions = {
            'create_user': self.create_user,
            'login': self.login_user,
            'logout': self.logout_user
        }

    def open(self):
        """defines the websocket open method"""
        pass

    @gen.coroutine
    def on_message(self, message):
        """defines the response to income messages"""
        data = json.loads(message)
        action = data.get('action')
        if action:
            self.service_functions[action](message)
        else:
            print('[channelHandler]: must give an action')
            self.write_message(
                json.dumps({'error': [0, 'there is no action in request']})
            )
        self.write_message(message)

    def on_close(self):
        """defines the websocket close method"""
        pass

    def create_user(self, message):
        # IMPLEMETAR LOGICA DEL SERVICIO AQUI
        pass

    def login_user(self, message):
        # IMPLEMETAR LOGICA DEL SERVICIO AQUI
        pass

    def logout_user(self, message):
        # IMPLEMETAR LOGICA DEL SERVICIO AQUI
        pass
