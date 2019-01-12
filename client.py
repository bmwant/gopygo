import curses
import xmlrpc.client
from curses import wrapper
from functools import partial


HOST = 'dex.local'
PORT = 8777

from Tkinter import *

master = Tk()
master.wm_title('GoPiGo3')

width = 1000
height = 600
circle = [width / 2, height / 2, width / 2 + 50, height / 2 + 50]

canvas = Canvas(master, width=width, height=height, bg="White")


def print_top(stdscr, message):
    stdscr.clear()
    stdscr.addstr(0, 0, message)
    stdscr.refresh()


def main(stdscr, *args, **kwargs):
    s = xmlrpc.client.ServerProxy('http://{host}:{port}'.format(host=HOST, port=PORT))
    # print(s.system.listMethods())
    # stdscr = curses.initscr()
    # do not echo keys to the screen
    curses.noecho()
    # do not require enter to be pressed
    curses.cbreak()
    print_ = partial(print_top, stdscr)
    print_('Use w/a/s/d keys to navigate your robot')

    canvas.bind('<KeyRelease-w>', s.stop)
    canvas.bind('<KeyRelease-s>', s.stop)

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
    wrapper(main)
