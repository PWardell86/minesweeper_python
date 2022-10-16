from tkinter import StringVar, ttk, Tk, mainloop

class Label(ttk.Label):
    def __init__(self, backgroundImage, **kwargs):
        super(Label, self).__init__(**kwargs)
        self.image = backgroundImage