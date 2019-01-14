import time
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.pressed = False
        self._stamp_pressed = 0
        self._stamp_released = 0
        self.c = 0

    def create_widgets(self):
        self.hi_there = tk.Button(self, repeatdelay=0, repeatinterval=0)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        self.master.bind('<KeyRelease-s>', self.say_released)

        self.master.bind('<KeyPress-s>', self.say_press)

    def say_press(self, event):
        print('Pressed')
        # import pdb; pdb.set_trace()
        return 'break'

    def say_released(self, event=None):
        print('Released')
        return 'break'


if __name__ == '__main__':
    import os
    os.system('xset r off')
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    os.system('xset r on')