import os
import tkinter as tk
from functools import partial


class TkControlWrapper(tk.Frame):
    def __init__(self, controller, master=None):
        self.master = master or tk.Tk()
        super().__init__(self.master)

        os.system('xset r off')
        self.c = controller
        self.master.geometry('300x200')
        self.master.resizable(0, 0)
        self.pack()
        self.master.title('GoPiGo Controls')
        self.create_widgets()
        self.bind_controls()

    def __del__(self):
        os.system('xset r on')
        self.c.close()

    def create_widgets(self):
        w2 = tk.Scale(self.master, from_=0, to=500,
                      tickinterval=100, length=300, orient=tk.HORIZONTAL, command=self.c.set_speed)
        w2.set(300)  # default speed
        w2.pack(side='top')
        self.quit = tk.Button(self, text='exit',
                              command=self.master.destroy)
        self.quit.pack(side='bottom')

    def bind_controls(self):
        self.master.bind('<KeyPress-w>',    partial(self.wrap_event, self.c.forward))
        self.master.bind('<KeyPress-s>',    partial(self.wrap_event, self.c.backward))
        self.master.bind('<KeyRelease-w>',  partial(self.wrap_event, self.c.stop))
        self.master.bind('<KeyRelease-s>',  partial(self.wrap_event, self.c.stop))
        self.master.bind('<KeyPress-a>',    partial(self.wrap_event, self.c.left))
        self.master.bind('<KeyPress-d>',    partial(self.wrap_event, self.c.right))
        self.master.bind('<space>',         partial(self.wrap_event, self.c.flash))
        self.master.bind('<KeyPress-l>',    partial(self.wrap_event, self.c.lights))

    def wrap_event(self, function, event):
        print(event)
        function()
