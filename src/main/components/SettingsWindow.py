from tkinter import StringVar, Tk, mainloop, ttk

BOTS = 3
class SettingsWindow(Tk):
    def __init__(self, theme):
        super(SettingsWindow, self).__init__("Settings", "300x400")
        themePath = f"../../resources/{theme}"
        bot = StringVar()
        values = [str(i + 1) for i in range(BOTS)]
        botSelector = ttk.OptionMenu(self, bot, "0", *values)
        botSelector.grid(column=0, row=0)
        mainloop()

SettingsWindow("Default")
