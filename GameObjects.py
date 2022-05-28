from pyglet import sprite, text, graphics
from tkinter import *
from tkinter import ttk
import os


class Counter(text.Label):
    def __init__(self, x, y, batch, initial=0, font="Joystix Monospace", fontSize=20, color=(0, 200, 0, 255)):
        super(Counter, self).__init__(
            str(initial),
            font_name=font, font_size=fontSize, color=color,
            anchor_x="center", anchor_y="center", x=x, y=y,
            batch=batch, group=graphics.OrderedGroup(1))  # Move it to the top so it can be seen
        self.locked = False
        self.count = initial

    def plus(self):
        if self.locked: return
        self.count += 1
        self.text = str(self.count)

    def minus(self):
        if self.locked: return
        self.count -= 1
        self.text = str(self.count)

    def setCounter(self, count):
        if self.locked: return
        self.count = count
        self.text = str(count)


class Tile(sprite.Sprite):
    def __init__(self, x, y, size, defaultImage, batch, value=None, isRevealed=False, isFlagged=False):
        self.isRevealed = isRevealed
        self.isFlagged = isFlagged
        self.value = value
        # defaultImage.anchor_x = defaultImage.width / 2
        # defaultImage.anchor_y = defaultImage.height / 2
        super(Tile, self).__init__(defaultImage, x, y, batch=batch)
        
        # Scale the tile properly
        self.scale = size / self.width


class Button(sprite.Sprite):
    def __init__(self, x, y, restImage, pressedImage, width, height, command, batch):
        super(Button, self).__init__(restImage, x, y, batch=batch)
        self.batch = batch
        self.scale_x = width / self.width
        self.scale_y = height / self.height
        self.restImage = restImage
        self.pressedImage = pressedImage
        self.command = command

    def clickEvent(self, cx, cy, released):
        if (cx > self.x and cx < (self.x + self.width) and
                cy > self.y and cy < (self.y + self.height)):
            if released == 0:
                self.image = self.pressedImage
            if released == 1:
                self.image = self.restImage
                self.command()


class SettingsWindow(Tk):
    def __init__(self, saveCommand, theme="Star Wars 2", width=250, height=300, name="Settings"):
        super(SettingsWindow, self).__init__("Settings")
        self.wm_attributes('-toolwindow', True)
        self.saveCommand = saveCommand
        self.title(name)

        self.setDiff = 0
        self.sclDiff = DoubleVar()

        path = "../2.0/Themes"
        themes = os.listdir(path)
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

        def lblDiffUpdate(s):
            self.lblDiffText.set(f"Difficulty: {s[:4]}")

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
