from pyglet import *
from random import random
from SettingsWindow import SettingsWindow
from GameButton import GameButton
from Tile import Tile
from Counter import Counter
from os import path

working_dir = path.dirname(path.realpath(__file__))
resource.path = [working_dir, path.realpath('resources')]

def button_size(h):
    return h / 1.5

class Minesweeper(window.Window):
    def __init__(self, theme="Default", difficulty=0.25, gameSize=(10, 10), windowSize=(500, 500)):
        """
        Extends pyglet.window.Window and contains a minesweeper game.
        - theme: The name of the folder that contains the theme to use
        - difficulty: The fraction of tiles that will be bombs, defaults to 0.25, medium
        - gameSize: The width and height of the game given in the nuber of tiles
        - windowSize: The size of the actual window
        """
        super(Minesweeper, self).__init__(
            windowSize[0], windowSize[1], caption="Minesweeper", style='dialog')
        self.themeDir = theme
        self.batch = graphics.Batch()

        self.tiles = []
        self.difficulty = difficulty
        self.gameSize = gameSize
        self.started = False
        self.gameOver = False

        # Initialize the top bar, and counters for timer and flags
        self.sprtTopBar = sprite.Sprite(resource.image(
            f"{self.themeDir}/TopBar.png"), batch=self.batch, group=graphics.OrderedGroup(1))
        self.barHeight = self.sprtTopBar.height
        self.sprtTopBar.y = self.height - self.barHeight
        self.sprtTopBar.scale_x = self.width / self.sprtTopBar.width

        self.tileSize = min(
            windowSize[0] // gameSize[0], (windowSize[1] - self.barHeight) // gameSize[1])
        self.emptySpace = [
            (self.width - (self.gameSize[0] * self.tileSize)) / 2,
            (self.height - self.barHeight -
             (self.gameSize[1] * self.tileSize)) / 2
        ]

        # Initialize the buttons for a new game and settings
        pImage = resource.image(f"{self.themeDir}/settings0.png")
        rImage = resource.image(f"{self.themeDir}/settings1.png")
        bSize = button_size(self.barHeight)
        bYLoc = (self.height - (self.barHeight) / 2) - bSize / 2
        def btnCommand(): return SettingsWindow(self.save)

        self.btnSettings = GameButton(self.width / 2 - (bSize + 4), bYLoc,
                                      rImage, pImage, bSize, bSize, btnCommand, self.batch)

        pImage = resource.image(f"{self.themeDir}/newGame0.png")
        rImage = resource.image(f"{self.themeDir}/newGame1.png")
        self.btnNewGame = GameButton((self.width / 2), bYLoc,
                                     rImage, pImage, bSize, bSize, self.reset, self.batch)

        self.cntTimer = Counter(
            self.width / 3, self.height - (self.barHeight / 2), self.batch)

        self.cntFlags = Counter(
            2 * self.width / 3, self.height - (self.barHeight / 2), self.batch)

        # Contains the images for each tile value
        self.themeKey = {0: resource.image(f"{self.themeDir}/none.png"),
                         1: resource.image(f"{self.themeDir}/one.png"),
                         2: resource.image(f"{self.themeDir}/two.png"),
                         3: resource.image(f"{self.themeDir}/three.png"),
                         4: resource.image(f"{self.themeDir}/four.png"),
                         5: resource.image(f"{self.themeDir}/five.png"),
                         6: resource.image(f"{self.themeDir}/six.png"),
                         7: resource.image(f"{self.themeDir}/seven.png"),
                         8: resource.image(f"{self.themeDir}/eight.png"),
                         9: resource.image(f"{self.themeDir}/bomb.png"),
                         10: resource.image(f"{self.themeDir}/blank.png")}

        # Generate unrevealed tiles with no other values as a palceholder until the game is started
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):
                newTile = Tile(x * self.tileSize + self.emptySpace[0], y * self.tileSize + self.emptySpace[1],
                               self.tileSize, self.themeKey[10],
                               self.batch, None)
                row += [newTile]
            self.tiles += [row]

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def save(self, theme, difficulty, gameSize, winSize):
        self.themeDir = theme
        self.setTheme(theme)
        self.difficulty = difficulty
        self.gameSize = gameSize
        self.width = winSize[0]
        self.height = winSize[1]
        self.reset()

    def generateTiles(self, startX, startY):
        """
        Generates a random board for a game of minesweeper
        - startX, startY: The tile coordinates of the first tile clicked
        """
        self.tiles = []
        tilesRemaining = self.gameSize[0] * self.gameSize[1]
        bombsRemaining = tilesRemaining * self.difficulty

        # Generate the bombs
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):

                # Do not place any bombs within a radius of one of the clicked position
                # This is done so the start of the game is easier
                dx = abs(x - startX)
                dy = abs(y - startY)
                value = None
                if dx > 1 or dy > 1:
                    # The chance of a tile being a bomb is equal to:
                    # The number of bombs left to place divided by the number of tiles left to look over
                    bombChance = bombsRemaining / tilesRemaining
                    if bombChance >= random():
                        value = 9
                        bombsRemaining -= 1

                newTile = Tile(x * self.tileSize + self.emptySpace[0], y * self.tileSize + self.emptySpace[1],
                               self.tileSize, self.themeKey[10],
                               self.batch, value)
                tilesRemaining -= 1
                row += [newTile]
            self.tiles += [row]

        # Calculate the tile values
        for y in range(self.gameSize[1]):
            for x in range(self.gameSize[0]):
                if self.tiles[y][x].value == None:
                    bombsNear = 0
                    # The value of each tile that isnt a bomb is equal to the number of bombs adjacent to it
                    for nearTile in self.getNearTiles(x, y):
                        if nearTile.value == 9:
                            bombsNear += 1
                    self.tiles[y][x].value = bombsNear

    def getNearTiles(self, x, y):
        """
        Returns all tiles adjacent to the tile at [y][x] in self.tiles
        - Can return 4, 6, or 9 tiles
        """
        nearTiles = []
        for px in range(x - 1, x + 2):
            for py in range(y - 1, y + 2):
                if px != x or py != y:
                    if px >= 0 and px < self.gameSize[0] and py >= 0 and py < self.gameSize[1]:
                        nearTiles += [self.tiles[py][px]]
        return nearTiles

    def startGame(self, startX, startY):
        """
        Starts the game at the given tile coordinate
        """
        self.started = True
        self.cntTimer.locked = False
        self.cntTimer.locked = False
        self.generateTiles(startX, startY)
        self.revealTile(startX, startY)

    def endGame(self):
        """
        Ends the game. Resets the timer, flag count, score and board.
        """
        self.btnNewGame.image = resource.image(
            f"{self.themeDir}/newGameLost1.png")
        score = 0
        self.gameOver = True
        self.cntTimer.locked = True
        self.cntTimer.locked = True
        for row in self.tiles:
            for tile in row:
                if tile.value == 9:
                    if tile.isFlagged:
                        score += 1
                    elif not(tile.isRevealed):
                        tile.image = self.themeKey[9]

    def setTheme(self, name):
        """
        Updates the theme of the game to the given folder, name
        """
        # Set the theme of the game theme folder
        self.themeKey = {0: resource.image(f"{self.themeDir}/none.png"),
                         1: resource.image(f"{self.themeDir}/one.png"),
                         2: resource.image(f"{self.themeDir}/two.png"),
                         3: resource.image(f"{self.themeDir}/three.png"),
                         4: resource.image(f"{self.themeDir}/four.png"),
                         5: resource.image(f"{self.themeDir}/five.png"),
                         6: resource.image(f"{self.themeDir}/six.png"),
                         7: resource.image(f"{self.themeDir}/seven.png"),
                         8: resource.image(f"{self.themeDir}/eight.png"),
                         9: resource.image(f"{self.themeDir}/bomb.png"),
                         10: resource.image(f"{self.themeDir}/blank.png")}

    def reset(self):
        """
        Resets the game to its initial state with all class variables
        """
        # Resets the game
        self.started = False
        self.gameOver = False
        self.cntFlags.text = "0"
        self.tiles = []
        self.tileSize = min(
            self.width // self.gameSize[0], (self.height - self.barHeight) // self.gameSize[1])
        self.emptySpace = [
            (self.width - (self.gameSize[0] * self.tileSize)) / 2,
            (self.height - self.barHeight -
             (self.gameSize[1] * self.tileSize)) / 2
        ]

        self.sprtTopBar = sprite.Sprite(resource.image(
            f"{self.themeDir}/TopBar.png"), batch=self.batch, group=graphics.OrderedGroup(1))
        self.sprtTopBar.y = self.height - self.barHeight
        self.sprtTopBar.scale_x = self.width / self.sprtTopBar.width

        # Initialize the buttons for a new game and settings
        pImage = resource.image(f"{self.themeDir}/settings0.png")
        rImage = resource.image(f"{self.themeDir}/settings1.png")
        bSize = button_size(self.barHeight)
        bYLoc = (self.height - (self.barHeight) / 2) - bSize / 2
        def btnCommand(): return SettingsWindow(self.save)

        self.btnSettings = GameButton(self.width / 2 - (bSize + 4), bYLoc,
                                      rImage, pImage, bSize, bSize, btnCommand, self.batch)

        pImage = resource.image(f"{self.themeDir}/newGame0.png")
        rImage = resource.image(f"{self.themeDir}/newGame1.png")

        self.cntFlags.setCounter(0)
        self.cntFlags.setCounter(0)
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):
                newTile = Tile(x * self.tileSize + self.emptySpace[0], y * self.tileSize + self.emptySpace[1],
                               self.tileSize, self.themeKey[10],
                               self.batch, None)
                row += [newTile]
            self.tiles += [row]
        self.btnNewGame = GameButton((self.width / 2), bYLoc,
                                     rImage, pImage, bSize, bSize, self.reset, self.batch)

    def clickTile(self, x, y):
        if not(self.gameOver):
            self.autoClear(x, y)
            self.revealTile(x, y)

    def revealTile(self, x, y):
        """Reveals the tile at the given coordinate"""
        tile = self.tiles[y][x]
        if not(tile.isFlagged) and not(tile.isRevealed):
            tile.isRevealed = True
            tile.image = self.themeKey[tile.value]
            if tile.value == 0:
                self.clearBlanks(x, y)
            elif tile.value == 9:
                tile.image = resource.image(
                    f"{self.themeDir}/incorrectBomb.png")
                self.endGame()

    def autoClear(self, x, y):
        """
        If all the bombs around a revealed tile are flagged, this will reveal the rest of the tiles
        """
        tile = self.tiles[y][x]
        if tile.isRevealed:
            flagCount = 0
            for nearTile in self.getNearTiles(x, y):
                if nearTile.isFlagged:
                    flagCount += 1
            if flagCount == tile.value:
                for px in range(x - 1, x + 2):
                    for py in range(y - 1, y + 2):
                        if px != x or py != y:
                            if px >= 0 and px < self.gameSize[0] and py >= 0 and py < self.gameSize[1]:
                                self.revealTile(px, py)

    def flagTile(self, x, y):
        """
        Toggles whether or not the tile at the tile coordinates is flagged or not
        """
        # Flags the tile at the given coordinate
        tile = self.tiles[y][x]
        if tile.isFlagged:
            tile.isFlagged = False
            tile.image = self.themeKey[10]
            self.cntFlags.minus()
        elif tile.isRevealed is False:
            tile.isFlagged = True
            tile.image = resource.image(f"{self.themeDir}/flag.png")
            self.cntFlags.plus()

    def clearBlanks(self, x, y):
        """
        Recursively reveals all tiles surrounding a blank tile
        """
        # Clears the blanks around the revealed tile
        for px in range(x - 1, x + 2):
            for py in range(y - 1, y + 2):
                if px != x or py != y:
                    if px >= 0 and px < self.gameSize[0] and py >= 0 and py < self.gameSize[1]:
                        self.revealTile(px, py)
