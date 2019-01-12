import curses
import xmlrpc.client
from curses import wrapper


def main():
    s = xmlrpc.client.ServerProxy('http://localhost:8000')
    # print(s.system.listMethods())
    stdscr = curses.initscr()
    # do not echo keys to the screen
    curses.noecho()
    # do not require enter to be pressed
    curses.cbreak()

    try:
        c = stdscr.getkey()
        if c == 'w':
            print('Moving forward for 1 sec')
            s.forward()
        elif c == 's':
            print('Moving backward for 1 sec')
            s.backward()
        elif c == 'a':
            print('Turning left')
            s.left()
        elif c == 'f':
            print('Turning right')
            s.right()
        else:
            print('You have pressed', c)
    except KeyboardInterrupt:
        print('Shutting down a client')
        curses.nocbreak()
        curses.echo()
        curses.endwin()


if __name__ == '__main__':
    wrapper(main())
