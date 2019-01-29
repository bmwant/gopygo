import xmlrpc.client

from remote_controller import Controller
from tk_wrapper import TkControlWrapper
from speech_wrapper import SpeechControlWrapper


HOST = 'dex.local'
PORT = 8777


def main():
    s = xmlrpc.client.ServerProxy('http://{host}:{port}'.format(host=HOST, port=PORT))
    controller = Controller(s=s)
    # wrapper = TkControlWrapper(controller=controller)
    wrapper = SpeechControlWrapper(controller=controller)
    try:
        wrapper.mainloop()
    finally:
        del wrapper


if __name__ == '__main__':
    main()
