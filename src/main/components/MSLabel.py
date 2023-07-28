from tkinter import StringVar, Tk, mainloop, ttk


class Label(ttk.Label):
    def __init__(self, background_image, **kwargs):
        super(Label, self).__init__(**kwargs)
        self.image = background_image