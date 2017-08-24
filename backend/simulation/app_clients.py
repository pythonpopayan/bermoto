"""

"""
import websocket
import json
from time import sleep


class app_client(object):
    def __init__(self, url):
        self.ws = websocket.create_connection(url)

    def send(self, message):
        self.ws.send(json.dumps(message))
        sleep(0.5)
        result = self.ws.recv()
        print(result)
        return json.loads(result)

    def close(self):
        self.ws.close()
