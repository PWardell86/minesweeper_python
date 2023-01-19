from tkinter import StringVar, ttk, Tk, mainloop
from os import listdir
import sys


class SettingsWindow(Tk):
    def __init__(self,  saveCommand, width=250, height=300):
        super(SettingsWindow,self) .__init__("Game Configuration", f"{width}x{height}")
        self.wm_attributes("-toolwindow", True)
        self.saveCommand = saveCommand
        self.difficulty = 0.16

        path = "../../resources"
        themes = listdir(path)
        frm_buttons = ttk.Frame(self)
        frm_buttons.grid(column=0, row=1)

        frame_input = ttk.Frame(self)
        frame_input.grid(column=0, row=0)

        # Make the text labels for the inputs
        self.label_windowSize = ttk.Label(frame_input, text="Window Size: ")
        self.label_gameSize = ttk.Label(frame_input, text="Game Size: ")
        label_difficultyText = StringVar(frame_input, value=f"Difficulty: {self.difficulty}")
        self.label_difficulty = ttk.Label(
            frame_input, textvariable=label_difficultyText, width=14)
        self.label_theme = ttk.Label(frame_input, text="Theme: ")

        # Make the inputs
        self.combo_theme = ttk.Combobox(frame_input, values=themes)
        self.scale_difficulty = ttk.Scale(
            frame_input, value=0.16, from_=0, to=1,
            command=lambda v: self.lblDiffUpdate(v, label_difficultyText))
        self.entry_windowSize = ttk.Entry(frame_input)
        self.entry_gameSize = ttk.Entry(frame_input)

        # Format the items
        self.label_windowSize.grid(column=0, row=0, pady=5)
        self.label_gameSize.grid(column=0, row=1, pady=5)
        self.label_difficulty.grid(column=0, row=2, pady=5)
        self.label_theme.grid(column=0, row=3, pady=5)
        self.combo_theme.grid(column=1, row=3)
        self.scale_difficulty.grid(column=1, row=2)
        self.entry_windowSize.grid(column=1, row=0)
        self.entry_gameSize.grid(column=1, row=1)

        btnCancel = ttk.Button(
            frm_buttons, text="Cancel", command=self.destroy)
        btnSave = ttk.Button(
            frm_buttons, text="Save and Exit", command=self.save)
        btnCancel.grid(column=0, row=0)
        btnSave.grid(column=1, row=0)

        mainloop()

    def save(self):
        windowSizeRaw = self.entry_windowSize.get().split(", ")
        windowSize = []
        windowSize[0] = int(windowSizeRaw[0])
        windowSize[1] = int(windowSizeRaw[1])

        gameSizeRaw = self.entry_gameSize.get().split(", ")
        gameSize = []
        gameSize[0] = int(gameSizeRaw[0])
        gameSize[1] = int(gameSizeRaw[1])

        theme = self.combo_theme.get()
        if self.difficulty == 0:
            self.difficulty = 0.16
        self.destroy()
        self.saveCommand(theme, self.difficulty, gameSize, windowSize)

    def lblDiffUpdate(self, value, label_difficultyText):
        self.difficulty = float(value)
        # Only take the first 4 digits for difficulty: 0.00
        label_difficultyText.set(f"Difficulty: {value[:4]}")
