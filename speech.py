import speech_recognition as sr


class SpeecControlWrapper(object):
    def __init__(self):
        self.r = sr.Recognizer()
        device_index = sr.Microphone.list_microphone_names().index('sysdefault')
        self.mic = sr.Microphone(device_index=device_index)

    def mainloop(self):
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        print(r.recognize_google(audio))


commands = {
    'forward': 0,
    'backward': 0,
    'left': 2,
    'right': 3,
    'stop': 4,
    'flash': 5,
    'dim': 6,
}


