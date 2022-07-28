from tkinter import DoubleVar, StringVar, ttk, Tk, mainloop
from os import listdir


class SettingsWindow(Tk):
    def __init__(self, saveCommand, width=250, height=300, name="Settings"):
        super(SettingsWindow, self).__init__("Settings", f"{width}x{height}")
        self.wm_attributes("-toolwindow", True)
        self.saveCommand = saveCommand
        self.title(name)

        self.setDiff = 0
        self.sclDiff = DoubleVar()

        path = "resources"
        themes = listdir(path)
        self.frmButtons = ttk.Frame(self)
        self.frmButtons.grid(column=0, row=1)

        self.frame_input = ttk.Frame(self)
        self.frame_input.grid(column=0, row=0)

        self.label_windowSize = ttk.Label(self.frame_input, text="Window Size: ")
        self.label_gameSize = ttk.Label(self.frame_input, text="Game Size: ")
        self.label_difficultyText = StringVar(self.frame_input, value="Difficulty: 0.3")
        self.label_difficulty = ttk.Label(
            self.frame_input, textvariable=self.label_difficultyText, width=14)
        self.label_theme = ttk.Label(self.frame_input, text="Theme: ")

        def lblDiffUpdate(sliderValue: str):
            # Only take the first 4 digits for difficulty: 0.00
            self.label_difficultyText.set(f"Difficulty: {sliderValue[:4]}")

        self.combo_theme = ttk.Combobox(self.frame_input, values=themes)
        self.scale_difficulty = ttk.Scale(
            self.frame_input, value=0.3, from_=0, to=1, variable=self.sclDiff, command=lblDiffUpdate)
        self.entry_windowSize = ttk.Entry(self.frame_input)
        self.entry_gameSize = ttk.Entry(self.frame_input)

        self.label_windowSize.grid(column=0, row=0, pady=5)
        self.label_gameSize.grid(column=0, row=1, pady=5)
        self.label_difficulty.grid(column=0, row=2, pady=5)
        self.label_theme.grid(column=0, row=3, pady=5)

        self.combo_theme.grid(column=1, row=3)
        self.scale_difficulty.grid(column=1, row=2)
        self.entry_windowSize.grid(column=1, row=0)
        self.entry_gameSize.grid(column=1, row=1)

        def save():
            windowSize = self.entry_windowSize.get().split(", ")
            windowSize[0] = int(windowSize[0])
            windowSize[1] = int(windowSize[1])

            gameSize = self.entry_gameSize.get().split(", ")
            gameSize[0] = int(gameSize[0])
            gameSize[1] = int(gameSize[1])

            theme = self.combo_theme.get()
            difficulty = self.sclDiff.get()
            self.destroy()
            self.saveCommand(theme, difficulty, gameSize, windowSize)

        self.btnCancel = ttk.Button(
            self.frmButtons, text="Cancel", command=self.destroy)
        self.btnSave = ttk.Button(
            self.frmButtons, text="Save and Exit", command=save)
        self.btnCancel.grid(column=0, row=0)
        self.btnSave.grid(column=1, row=0)

        mainloop()
