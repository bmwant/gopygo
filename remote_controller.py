

class Controller(object):
    COMMANDS = (
        'forward',
        'backward',
        'stop',
        'left',
        'right',
        'flash',
        'lights',
        'set_speed',
    )

    def __init__(self, s):
        self.s = s
        self._flashing = False
        self._lights = False

    def __getattr__(self, item):
        if item not in self.__dict__ and item in self.COMMANDS:
            command = getattr(self.s, item)
            command()

        raise AttributeError("No such attribute '%s'" % item)

    def flash(self):
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

    def lights(self):
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

    def set_speed(self, value):
        # todo: do not set each value, update each 50?
        self.s.set_speed(value)

    def close(self):
        self.s('close')


if __name__ == '__main__':
    pass
