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
            (r'/mirror', channelHandler, dict(q=q)),
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
        print('[channel]: started connection')

    @gen.coroutine
    def on_message(self, message):
        """defines the response to income messages"""
        data = json.loads(message)
        action = data.get('action')
        if action:
            print(message)
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

        # 1. vaidar si la informacion esta completa
        # se necesita al menos: name, password
        # se pide tambien el correo, (trabajar en el modelo de bd de usuario)

        # 2. validar si usuario no existe
        # ir a la base de datos y ver si existe el user_name que llego
        # mandar mensaje de ya existente

        # 3. validar si esta bien la contraseña
        # minimo 8 caracteres, letras y numeros al menos
        # mandar un mensaje de contraseña mala

        # 4. crear objeto usuario si pasa todas las validaciones
        # completar con defaults datos no obtenidos

        # 5. almacenar informacion del usuario

        # 6. devolver una respuesta al cliente

        # TODO: definir modelo de base de datos (christian)

        # TODO: seleccionar orm (edwin)
        # TODO: validar si usuario existe (edwin)
        # TODO: crear registro de usuario (edwin)

        # TODO: completar datos del json para insercion (christian)

        # TODO: funcion de validar contraseña (christian)

        pass

    def login_user(self, message):
        # IMPLEMETAR LOGICA DEL SERVICIO AQUI
        pass

    def logout_user(self, message):
        # IMPLEMETAR LOGICA DEL SERVICIO AQUI
        pass
