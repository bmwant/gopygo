import os
import xmlrpc.client
import tkinter as tk

from remote_controller import Controller
from tk_wrapper import TkControlWrapper


HOST = 'dex.local'
PORT = 8777


def main():
    s = xmlrpc.client.ServerProxy('http://{host}:{port}'.format(host=HOST, port=PORT))
    controller = Controller(s=s)
    wrapper = TkControlWrapper(controller=controller)
    try:
        wrapper.mainloop()
    finally:
        del wrapper


if __name__ == '__main__':
    main()
