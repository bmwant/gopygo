import os
import tkinter as tk


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
        self.master.bind('<KeyPress-w>', self.c.forward)
        self.master.bind('<KeyPress-s>', self.c.backward)
        self.master.bind('<KeyRelease-w>', self.c.stop)
        self.master.bind('<KeyRelease-s>', self.c.stop)
        self.master.bind('<KeyPress-a>', self.c.left)
        self.master.bind('<KeyPress-d>', self.c.right)
        self.master.bind('<space>', self.c.flash)
        self.master.bind('<KeyPress-l>', self.c.lights)
