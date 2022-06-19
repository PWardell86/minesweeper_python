from tkinter import DoubleVar, StringVar, ttk, Tk, mainloop
from os import listdir

class SettingsWindow(Tk):
    def __init__(self, saveCommand, width=250, height=300, name="Settings"):
        super(SettingsWindow, self).__init__("Settings")
        self.wm_attributes('-toolwindow', True)
        self.saveCommand = saveCommand
        self.title(name)

        self.setDiff = 0
        self.sclDiff = DoubleVar()

        path = "resources"
        themes = listdir(path)
        self.frmButtons = ttk.Frame(self)
        self.frmButtons.grid(column=0, row=1)

        self.frmInput = ttk.Frame(self)
        self.frmInput.grid(column=0, row=0)

        self.lblWindowSize = ttk.Label(self.frmInput, text="Window Size: ")
        self.lblGameSize = ttk.Label(self.frmInput, text="Game Size: ")
        self.lblDiffText = StringVar(self.frmInput, value="Difficulty: 0.3")
        self.lblDifficulty = ttk.Label(
            self.frmInput, textvariable=self.lblDiffText, width=14)
        self.lblTheme = ttk.Label(self.frmInput, text="Theme: ")

        def lblDiffUpdate(sliderValue: str):
            self.lblDiffText.set(f"Difficulty: {sliderValue[:4]}")

        self.cmboTheme = ttk.Combobox(self.frmInput, values=themes)
        self.sclDifficulty = ttk.Scale(
            self.frmInput, value=0.3, from_=0, to=1, variable=self.sclDiff, command=lblDiffUpdate)
        self.entryWinSize = ttk.Entry(self.frmInput)
        self.entryGameSize = ttk.Entry(self.frmInput)

        self.lblWindowSize.grid(column=0, row=0, pady=5)
        self.lblGameSize.grid(column=0, row=1,  pady=5)
        self.lblDifficulty.grid(column=0, row=2,  pady=5)
        self.lblTheme.grid(column=0, row=3,  pady=5)

        self.cmboTheme.grid(column=1, row=3)
        self.sclDifficulty.grid(column=1, row=2)
        self.entryWinSize.grid(column=1, row=0)
        self.entryGameSize.grid(column=1, row=1)

        def save():
            winSize = self.entryWinSize.get().split(", ")
            winSize[0] = int(winSize[0])
            winSize[1] = int(winSize[1])

            gameSize = self.entryGameSize.get().split(", ")
            gameSize[0] = int(gameSize[0])
            gameSize[1] = int(gameSize[1])

            theme = self.cmboTheme.get()
            difficulty = self.sclDiff.get()
            self.destroy()
            self.saveCommand(theme, difficulty, gameSize, winSize)

        self.btnCancel = ttk.Button(
            self.frmButtons, text="Cancel", command=self.destroy)
        self.btnSave = ttk.Button(
            self.frmButtons, text="Save and Exit", command=save)
        self.btnCancel.grid(column=0, row=0)
        self.btnSave.grid(column=1, row=0)

        mainloop()