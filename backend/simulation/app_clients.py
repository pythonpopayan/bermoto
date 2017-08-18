"""

"""
import websocket
import json


class app_client(object):
    def __init__(self, url):
        self.ws = websocket.create_connection(url)

    def send(self, message):
        self.ws.send(json.dumps(user))
        result = self.ws.recv()
        return json.loads(result)

    def close(self):
        self.ws.close()
