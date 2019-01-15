import sys
import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from concurrent.futures import ThreadPoolExecutor

from easygopigo3 import EasyGoPiGo3  # importing the EasyGoPiGo3 class


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


HOST = '0.0.0.0'
PORT = 8777
FLASH_DELAY = 0.2


class GoPiGoController(object):
    def __init__(self):
        self.gpg = EasyGoPiGo3()  # instantiating a EasyGoPiGo3 object
        self.flashing = False
        self.launch_executor()  # flash LEDs in the background

    def launch_executor(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.flash_lights)

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
        while True:
            if self.flashing:
                self.gpg.open_left_eye()
                time.sleep(FLASH_DELAY)
                self.gpg.close_left_eye()
            time.sleep(FLASH_DELAY)

    def start_flash(self):
        self.flashing = True

    def stop_flash(self):
        self.flashing = False
        self.gpg.close_eyes()

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
        requestHandler=RequestHandler,
        allow_none=True,
    )
    server.register_introspection_functions()
    server.register_instance(GoPiGoController())

    # Run the server's main loop
    print('Serving XML-RPC on {host}:{port}'.format(host=HOST, port=PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)


if __name__ == '__main__':
    main()
