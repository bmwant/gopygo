# https://realpython.com/python-speech-recognition/
from operator import methodcaller

import speech_recognition as sr


class SpeechControlWrapper(object):
    def __init__(self, controller):
        self.c = controller
        self.r = sr.Recognizer()
        device_index = sr.Microphone.list_microphone_names().index('sysdefault')
        self.mic = sr.Microphone(device_index=device_index)

    def mainloop(self):
        while True:
            print('Listening to the command...')
            with self.mic as source:
                self.r.adjust_for_ambient_noise(source)
                audio = self.r.listen(source)

            try:
                command = self.get_command(audio)
                f = methodcaller(command)
                print('Executing', command)
                f(self.c)
            except ValueError:
                print('Cannot match to a command, try again')

    def get_command(self, audio):
        res = None
        try:
            res = self.r.recognize_google(audio, language='en-US', show_all=True)
        except sr.UnknownValueError:
            pass
        options = [a['transcript'] for a in res['alternative']] if res else []
        for command in options:
            if command in self.c.COMMANDS:
                return command
        print('Recognized', res)
        raise ValueError('Unknown command')
