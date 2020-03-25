import sys
import time
import random
from http import HTTPStatus
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock
from functools import partial

from easygopigo3 import EasyGoPiGo3  # importing the EasyGoPiGo3 class


uprint = partial(print, flush=True)


class SingleClientRequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    _client = None

    def handle(self):
        client_host, client_port = self.client_address
        if self.check_client(client_host):
            super().handle()
        else:
            self.send_error(
                HTTPStatus.TOO_MANY_REQUESTS,
                'Only single client is supported'
            )

    def check_client(self, host):
        if self._client is None:
            self._client = host

        return host == self._client


HOST = '0.0.0.0'
PORT = 8777
FLASH_DELAY = 0.1


class GoPiGoController(object):
    def __init__(self, mock_controls=False):
        if mock_controls:
            self.gpg = MagicMock()
        else:
            self.gpg = EasyGoPiGo3()  # instantiating a EasyGoPiGo3 object
        self.gpg = MagicMock()  # instantiating a EasyGoPiGo3 object
        self.flashing = False
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.executor.submit(self.flash_lights)

    def cleanup(self):
        uprint('Cleaning up...')
        self.executor.shutdown(wait=False)
        self.stop()
        self.stop_flash()

    def __del__(self):
        self.cleanup()

    def forward(self):
        self.gpg.forward()

    def backward(self):
        self.gpg.backward()

    def left(self):
        self.gpg.turn_degrees(-90)

    def right(self):
        self.gpg.turn_degrees(90)

    def stop(self):
        self.gpg.stop()

    def set_speed(self, value):
        self.gpg.set_speed(value)

    def flash_lights(self):
        gpg = self.gpg
        led_triggers = (
            (gpg.open_left_eye, gpg.close_left_eye),
            (gpg.open_right_eye, gpg.close_right_eye),
            (partial(gpg.blinker_on, 0), partial(gpg.blinker_off, 0)),
            (partial(gpg.blinker_on, 1), partial(gpg.blinker_off, 1)),
        )
        leds = len(led_triggers)
        flags = [False] * leds
        while True:
            if self.flashing:
                led = random.randrange(0, leds)
                action = not flags[led]
                flags[led] = action
                led_triggers[led][action]()
                time.sleep(FLASH_DELAY)
            else:
                time.sleep(1)

    def start_flash(self):
        self.flashing = True

    def stop_flash(self):
        self.flashing = False
        self.turn_lights_off()

    def turn_lights_on(self):
        self.gpg.open_eyes()
        self.gpg.blinker_on(0)
        self.gpg.blinker_on(1)

    def turn_lights_off(self):
        self.gpg.close_eyes()
        self.gpg.blinker_off(0)
        self.gpg.blinker_off(1)


def main():
    # Create server
    # commented block is for 3.7
    # with SimpleXMLRPCServer(('localhost', 8000),
    #                         requestHandler=RequestHandler) as server:
    server = SimpleXMLRPCServer(
        (HOST, PORT),
        requestHandler=SingleClientRequestHandler,
        allow_none=True,
    )
    server.register_introspection_functions()
    controller = GoPiGoController()
    server.register_instance(controller)

    # Run the server's main loop
    uprint('Serving XML-RPC on {host}:{port}'.format(host=HOST, port=PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        uprint('\nKeyboard interrupt received, exiting.')
        server.shutdown()
        controller.cleanup()
        sys.exit(0)
    finally:
        del controller


if __name__ == '__main__':
    main()
