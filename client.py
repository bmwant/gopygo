import os
import curses
import xmlrpc.client
import tkinter as tk
from curses import wrapper
from functools import partial


HOST = 'dex.local'
PORT = 8777


class Application(tk.Frame):
    def __init__(self, s, master=None):
        super().__init__(master)
        os.system('xset r off')
        self.s = s
        self.master = master
        self.master.geometry('300x200')
        self.master.resizable(0, 0)
        self.pack()
        self.master.title('GoPiGo Controls')
        self.create_widgets()
        self.bind_controls()

    def __del__(self):
        os.system('xset r on')

    def create_widgets(self):
        self.quit = tk.Button(self, text='exit',
                              command=self.master.destroy)
        self.quit.pack(side='bottom')

    def bind_controls(self):
        self.master.bind('<KeyPress-w>', partial(self.wrap_event, self.s.forward))
        self.master.bind('<KeyPress-s>', partial(self.wrap_event, self.s.backward))
        self.master.bind('<KeyRelease-w>', partial(self.wrap_event, self.s.stop))
        self.master.bind('<KeyRelease-s>', partial(self.wrap_event, self.s.stop))
        self.master.bind('<KeyPress-a>', partial(self.wrap_event, self.s.left))
        self.master.bind('<KeyPress-d>', partial(self.wrap_event, self.s.right))

    def wrap_event(self, function, event):
        print(event)
        function()


def print_top(stdscr, message):
    stdscr.clear()
    stdscr.addstr(0, 0, message)
    stdscr.refresh()


def main():
    s = xmlrpc.client.ServerProxy('http://{host}:{port}'.format(host=HOST, port=PORT))
    root = tk.Tk()
    app = Application(s=s, master=root)
    try:
        app.mainloop()
    finally:
        del app


def main_curses(stdscr, *args, **kwargs):
    s = xmlrpc.client.ServerProxy('http://{host}:{port}'.format(host=HOST, port=PORT))
    # print(s.system.listMethods())
    # stdscr = curses.initscr()
    # do not echo keys to the screen
    curses.noecho()
    # do not require enter to be pressed
    curses.cbreak()
    print_ = partial(print_top, stdscr)
    print_('Use w/a/s/d keys to navigate your robot')

    try:
        while True:
            c = stdscr.getkey()
            if c == 'w':
                print_('Moving forward for 1 sec')
                s.forward()
            elif c == 's':
                print_('Moving backward for 1 sec')
                s.backward()
            elif c == 'a':
                print_('Turning left')
                s.left()
            elif c == 'd':
                print_('Turning right')
                s.right()
            else:
                print('You have pressed', c)
    except KeyboardInterrupt:
        print('Shutting down a client')
        curses.nocbreak()
        curses.echo()
        curses.endwin()


if __name__ == '__main__':
    # wrapper(main_curses)
    main()
