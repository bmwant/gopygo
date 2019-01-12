import sys
import time
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from easygopigo3 import EasyGoPiGo3  # importing the EasyGoPiGo3 class


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


HOST = '0.0.0.0'
PORT = 8777


class GoPiGoController(object):
    def __init__(self):
        self.gpg = EasyGoPiGo3()  # instantiating a EasyGoPiGo3 object

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