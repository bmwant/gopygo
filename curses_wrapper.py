import curses
from curses import wrapper


def print_top(stdscr, message):
    stdscr.clear()
    stdscr.addstr(0, 0, message)
    stdscr.refresh()


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
    wrapper(main_curses)
