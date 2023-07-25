from tkinter import StringVar, ttk, Tk, mainloop

class Label(ttk.Label):
    def __init__(self, background_image, **kwargs):
        super(Label, self).__init__(**kwargs)
        self.image = background_image