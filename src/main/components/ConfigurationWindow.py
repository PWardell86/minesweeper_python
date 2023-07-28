import sys
from os import listdir
from tkinter import StringVar, Tk, mainloop, ttk

from main.utils.Logger import Logger


class ConfigWindow(Tk):
    def __init__(self,  save_command, theme_dir, width=250, height=300):
        super(ConfigWindow,self) .__init__("Game Configuration", f"{width}x{height}")
        self.LOG = Logger(self)
        self.LOG.debug(sys.path)
        self.title("Config")
        self.save_command = save_command
        self.difficulty = 0.16
        
        themes = listdir(theme_dir)
        frm_buttons = ttk.Frame(self)
        frm_buttons.grid(column=0, row=1)

        frame_input = ttk.Frame(self)
        frame_input.grid(column=0, row=0)

        # Make the text labels for the inputs
        self.label_windowSize = ttk.Label(frame_input, text="Window Size: ")
        self.label_gameSize = ttk.Label(frame_input, text="Game Size: ")
        lbl_diff_text = StringVar(frame_input, value=f"Difficulty: {self.difficulty}")
        self.label_difficulty = ttk.Label(
            frame_input, textvariable=lbl_diff_text, width=14)
        self.label_theme = ttk.Label(frame_input, text="Theme: ")

        # Make the inputs
        self.combo_theme = ttk.Combobox(frame_input, values=themes)
        self.scale_difficulty = ttk.Scale(frame_input, value=0.16, from_=0, to=1, command=lambda v: self.lblDiffUpdate(v, lbl_diff_text))
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

        btnCancel = ttk.Button(frm_buttons, text="Cancel", command=self.destroy)
        btnSave = ttk.Button(frm_buttons, text="Save and Exit", command=self.save)
        btnCancel.grid(column=0, row=0)
        btnSave.grid(column=1, row=0)

        mainloop()

    def save(self):
        try:
            windowSize = self.getAndValidateEntryInput(self.entry_windowSize)
            gameSize = self.getAndValidateEntryInput(self.entry_gameSize)
        except ValueError:
            self.entry_windowSize.delete(0, -1)
            self.entry_gameSize.delete(0, -1)
            return

        theme = self.combo_theme.get()
        if self.difficulty == 0:
            self.difficulty = 0.16
        self.destroy()
        self.save_command(theme, self.difficulty, gameSize, windowSize)

    def lblDiffUpdate(self, value, lbl_diff_text):
        self.difficulty = float(value)
        lbl_diff_text.set(f"Difficulty: {value[:4]}")

    def getAndValidateEntryInput(self, entry):
        split_input = entry.get().split(",")
        return [int(value.strip()) for value in split_input]
