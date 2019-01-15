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
        self._flashing = False
        self._lights = False

    def __del__(self):
        os.system('xset r on')

    def create_widgets(self):
        w2 = tk.Scale(self.master, from_=0, to=500,
                      tickinterval=100, length=300, orient=tk.HORIZONTAL, command=self.set_speed)
        w2.set(300)  # default speed
        w2.pack(side='top')
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
        self.master.bind('<KeyPress-k>', self.flash)
        self.master.bind('<KeyPress-l>', self.lights)

    def wrap_event(self, function, event):
        print(event)
        function()

    def set_speed(self, value):
        # todo: do not set each value, update each 50?
        self.s.set_speed(value)

    def flash(self, event):
        if self._lights:
            print('Cannot flash when lights is on!')
            return

        if self._flashing:
            self._flashing = False
            self.s.stop_flash()
            print('Stop flashing')
            return

        self.s.start_flash()
        print('Start flashing')
        self._flashing = True

    def lights(self, event):
        if self._flashing:
            print('Cannot turn lights on when flashing!')
            return

        if self._lights:
            self._lights = False
            self.s.turn_lights_off()
            print('Lights is off')
            return

        self.s.turn_lights_on()
        print('Lights is on')
        self._lights = True


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
