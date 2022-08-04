from tkinter import DoubleVar, StringVar, ttk, Tk, mainloop
from os import listdir


class SettingsWindow(Tk):
    def __init__(self,  saveCommand, width=250, height=300, name="Settings"):
        super(SettingsWindow,self) .__init__("Settings", f"{width}x{height}")
        self.wm_attributes("-toolwindow", True)
        self.title(name)
        path = "../resources"
        themes = listdir(path)
        frmButtons = ttk.Frame(self)
        frmButtons.grid(column=0, row=1)

        frame_input = ttk.Frame(self)
        frame_input.grid(column=0, row=0)

        self.difficulty = 0.16
        label_windowSize = ttk.Label(frame_input, text="Window Size: ")
        label_gameSize = ttk.Label(frame_input, text="Game Size: ")
        label_difficultyText = StringVar(frame_input, value=f"Difficulty: {self.difficulty}")
        label_difficulty = ttk.Label(
            frame_input, textvariable=label_difficultyText, width=14)
        label_theme = ttk.Label(frame_input, text="Theme: ")

        def lblDiffUpdate(value):
            self.difficulty = float(value)
            # Only take the first 4 digits for difficulty: 0.00
            label_difficultyText.set(f"Difficulty: {value[:4]}")

        combo_theme = ttk.Combobox(frame_input, values=themes)
        scale_difficulty = ttk.Scale(
            frame_input, value=0.16, from_=0, to=1, command=lblDiffUpdate)
        entry_windowSize = ttk.Entry(frame_input)
        entry_gameSize = ttk.Entry(frame_input)

        label_windowSize.grid(column=0, row=0, pady=5)
        label_gameSize.grid(column=0, row=1, pady=5)
        label_difficulty.grid(column=0, row=2, pady=5)
        label_theme.grid(column=0, row=3, pady=5)

        combo_theme.grid(column=1, row=3)
        scale_difficulty.grid(column=1, row=2)
        entry_windowSize.grid(column=1, row=0)
        entry_gameSize.grid(column=1, row=1)

        def save():
            windowSize = entry_windowSize.get().split(", ")
            windowSize[0] = int(windowSize[0])
            windowSize[1] = int(windowSize[1])

            gameSize = entry_gameSize.get().split(", ")
            gameSize[0] = int(gameSize[0])
            gameSize[1] = int(gameSize[1])

            theme = combo_theme.get()
            if self.difficulty == 0:
                self.difficulty = 0.16
            self.destroy()
            saveCommand(theme, self.difficulty, gameSize, windowSize)

        btnCancel = ttk.Button(
            frmButtons, text="Cancel", command=self.destroy)
        btnSave = ttk.Button(
            frmButtons, text="Save and Exit", command=save)
        btnCancel.grid(column=0, row=0)
        btnSave.grid(column=1, row=0)

        mainloop()
