"""
backend functions

- crearse perfil
- mandar pedido
- comunicar pedido
- aceptar pedido
- cancelar pedido
- pedido cumplido
"""
import os
import json
import websocket
from copy import deepcopy
from time import sleep
from subprocess import Popen
from unittest import TestCase, skip

from simulation.app_clients import app_client


class mirroring_testing(TestCase):

    def setUp(self):
        """
        inicia el servicio del backend y hace configuraciones iniciales
        de los tests
        """
        backend_file_location = os.path.join(
            os.path.dirname(__file__),
            '..',
            'app.py'
        )
        # start backend service
        self.backend_service = Popen(
            ['python', '-OO', backend_file_location]
        )
        sleep(3)

    def tearDown(self):
        """
        termina el servicio del backend y elimina todo rastro de los Tests
        """
        self.backend_service.kill()
        sleep(3)

    def test_mirroring(self):
        """
        prueba una comunicacion websocket para explicar como interactua esta
        con el servidor de la aplicacion, test basico para ver que servidor
        y banco de pruebas funcionan bien
        """
        message = 'howdy'
        ws = websocket.create_connection('ws://0.0.0.0:8080/mirror')
        ws.send(message)
        result = ws.recv()
        self.assertEqual(
            message,
            result,
            msg='message and server response must be the same'
            )
        print('[test_mirroring]: server said: {}'.format(result))
        ws.close()


class app_testing(TestCase):

    def setUp(self):
        """
        inicia el servicio del backend y hace configuraciones iniciales
        de los tests
        """
        backend_file_location = os.path.join(
            os.path.dirname(__file__),
            '..',
            'app.py'
        )
        # start backend service
        self.backend_service = Popen(
            ['python', '-OO', backend_file_location, '--port=8080']
        )
        sleep(3)
        # simular un cliente
        self.client = app_client('ws://0.0.0.0:8080/channel')
        # datos dummy para usar
        self.dummy_user_info = {
            'user_name': 'andreu',
            'password': 'buenafuente',
            'action': 'create_user'
        }

    def tearDown(self):
        """
        termina el servicio del backend y elimina todo rastro de los Tests
        """
        self.client.close()
        self.backend_service.kill()
        sleep(3)

    def test_crear_perfil(self):
        """
        enviar la informacion de un usuario que no existe y obtener la
        confirmacion de que fue creado
        """
        # definir informacion de usuario, esta es la basica pero toca
        # investigar los datos que puede sacar el facebook
        user = {
            'user_name': 'berto',
            'password': 'romero',
            'action': 'create_user'
        }

        # CASO 1. REGISTRO DE UN USUARIO POR PRIMERA VEZ
        # debe registrar al usuario y regresar informacion que lo confirme
        response_data = self.client.send(user)
        # mirar si el usuario fue creado y si no hay errores
        self.assertEqual(response_data['error'], [0, 'ok'])  # 0 means no error
        self.assertEqual(response_data['action'], 'user_created')
        # la respuesta debe ser: {'action': 'user_created', 'error': [0, 'ok']}

        # CASO 2. REGISTRO DE UN USUARIO YA REGISTRADO
        # probar registrar a un usuario registrado, en este caso,
        # la plataforma debe mandar un error
        response_data = self.client.send(user)
        self.assertEqual(
            response_data['error'],
            [1, 'user already exists']  # 1 means failed doing an action
            )
        self.assertEqual(response_data['action'], 'failed_user_creation')

        # CASO 3. MALA INFORMACION PARA REGISTRO
        # si falta informacion para el registro, este no debe realizarse
        # para proteger a la plataforma de posibles registros peligrosos
        user = {
            'user_name': 'joel'
        }
        response_data = self.client.send(user)
        self.assertEqual(
            response_data['error'],
            [2, 'bad information in request']  # 2 means failed info validation
            )
        self.assertEqual(response_data['action'], 'failed_user_creation')

    def test_login_logout(self):
        """
        prueba de manera automatica la creacion de un usuario, su login y
        logout
        """
        # 1. crear usuario
        r = self.client.send(self.dummy_user_info)
        # 2. registrar usuario
        login_info = deepcopy(self.dummy_user_info)
        login_info['action'] = 'login'
        response_data = self.client.send(login_info)
        # mirar si devuelve un dato llamado session_token de 16 caracteres
        self.assertIn('session_token', response_data)
        self.assertEqual(response_data['error'], [0, 'ok'])
        self.assertEqual(len(response_data['session_token']), 16)
        self.assertEqual(response_data['action'], 'login_succesful')
        # 3. cerrar sesion de usuario
        logout_info = deepcopy(login_info)
        logout_info['action'] = 'logout'
        response_data = self.client.send(logout_info)
        self.assertEqual(response_data['error'], [0, 'ok'])
        self.assertEqual(response_data['action'], 'logout_succesful')

    def test_mandar_pedido(self):
        """
        crea un usuario y manda un pedido a la plataforma
        """
        # 1. crear usuario
        r = self.client.send(self.dummy_user_info)
        # 2. registrar usuario
        login_info = deepcopy(self.dummy_user_info)
        login_info['action'] = 'login'
        response_data = self.client.send(login_info)
        # 3. mandar pedido
        # CASO 1. PRIMER PEDIDO
        # debe ser atendido
        info_pedido = {
            'session_token': '1' * 16,  # token de sesion de 16 cifras
            'user_location': [1.222, 1.333] # coordenada notacion decimal
        }
        respuesta_pedido = self.client.send(info_pedido)
        # mirar si la respuesta al pedido esta bien
        self.assertEqual(response_data['error'], [0, 'ok'])
        self.assertEqual(respuesta_pedido['action'], 'pedido_activo')
        self.assertIn('token_pedido', respuesta_pedido)
        # el token_pedido es una cadena de 10 caracteres
        self.assertRegex(respuesta_pedido['token_pedido'], '\w{10}')
        # 4. cerrar sesion de usuario
        logout_info = deepcopy(login_info)
        logout_info['action'] = 'logout'
        response_data = self.client.send(logout_info)
        # CASO 2. SEGUNDO PEDIDO
        # no debe ser atendido porque ya hay uno en la plataforma
        respuesta_pedido = self.client.send(info_pedido)

    @skip('not implemented')
    def test_comunicar_pedido(self):
        """
        prueba para ver si un pedido es comunicado a alguno de los usurios
        conectados
        """
        # TODO: implementar este test, mejorar el simulador manteniendo compatibilidad
        # crear varios clientes y registrarlos
        # crear un cliente que envie el pedido
        # revisar si algun cliente recibio el pedido
        pass

    @skip('not implemented')
    def test_cancelar_pedido(self):
        """
        prueba para ver si se puede cancelar bien un pedido de parte del que
        lo pide o el que lo acepta y si estos cambios se transmiten a ambos,
        tambien prueba si se puede cancelar el pedido antes de que alguien lo
        acepte
        """
        # TODO: implementar, automatizar en el cliente el envio del pedido
        # crear un cliente para recibir el pedido configurado para que lo acepte
        # crear un cliente que envie el pedido
        # CASO 1. MANDAR Y CANCELAR EL PEDIDO
        # mandar el pedido
        # cancelar el pedido
        # CASO 2. MANDAR EL PEDIDO, ACEPTAR EL PEDIDO Y LUEGO CANCELARLO
        # DESDE EL QUE LO PIDE
        # mandar el pedido
        # aceptar el pedido
        # cancelar el pedido desde el que lo pide
        # CASO 3. MANDAR EL PEDIDO, ACEPTAR EL PEDIDO Y LUEGO CANCELARLO
        # DESDE EL QUE LO ACEPTA
        # mandar el pedido
        # aceptar el pedido
        # cancelar el pedido desde el que lo acepta
        pass

    @skip('not implemented')
    def test_aceptar_pedido(self):
        """
        prueba para ver que un cliente puede aceptar el pedido realizado por
        otro
        """
        # TODO: implementar este test, implementar el metodo aceptar_pedido en cliente
        # crear un cliente para recibir el pedido configurado para que lo acepte
        # crear un cliente que envie el pedido
        # mandar el pedido
        # revisar la informacion del cliente que acepta el pedido
        # revisar la informacion del cliente que hace el pedido
        # ver que las informacione anteriores sean validas
        pass

    @skip('not implemented')
    def test_pedido_cumplido(self):
        """
        prueba para mirar como funciona la terminacion exitosa del pedido
        """
        pass
