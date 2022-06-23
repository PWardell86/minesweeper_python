from pyglet import *
from random import random
from SettingsWindow import SettingsWindow
from GameButton import GameButton
from Tile import Tile
from Counter import Counter,Timer
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

        self.timer = Timer(
            self.width / 3, self.height - (self.barHeight / 2), self.batch)

        self.cntFlags = Counter(
            2 * self.width / 3, self.height - (self.barHeight / 2), self.batch)

        # Contains the images for each tile value
        self.themeKey = self.getThemeKey()

        # Generate unrevealed tiles with no other values as a palceholder until the game is started
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):
                newTile = Tile(x * self.tileSize + self.emptySpace[0], y * self.tileSize + self.emptySpace[1],
                               self.tileSize, self.themeKey[10],
                               self.batch, None)
                row += [newTile]
            self.tiles += [row]

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

    def setTheme(self, name):
        """
        Updates the theme of the game to the given folder, name
        """
        # Set the theme of the game theme folder
        self.themeDir = name
        self.themeKey = self.getThemeKey()

    def startGame(self, startX, startY):
        """
        Starts the game at the given tile coordinate
        """
        self.started = True
        self.timer.locked = False
        self.cntFlags.locked = False
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
        self.timer.locked = True
        for row in self.tiles:
            for tile in row:
                if tile.value == 9:
                    if tile.isFlagged:
                        score += 1
                    elif not(tile.isRevealed):
                        tile.image = self.themeKey[9]

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

    def getThemeKey(self):
        d = {0: "none.png",
             1: "one.png",
             2: "two.png",
             3: "three.png",
             4: "four.png",
             5: "five.png",
             6: "six.png",
             7: "seven.png",
             8: "eight.png",
             9: "bomb.png",
             10: "blank.png"}

        for key in d.keys():
            d[key] = resource.image(f"{self.themeDir}/{d[key]}")
        return d

    def save(self, theme, difficulty, gameSize, winSize):
        self.themeDir = theme
        self.setTheme(theme)
        self.difficulty = difficulty
        self.gameSize = gameSize
        self.width = winSize[0]
        self.height = winSize[1]
        self.reset()

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

        self.sprtTopBar = sprite.Sprite(
            resource.image(f"{self.themeDir}/TopBar.png"), batch=self.batch, group=graphics.OrderedGroup(1))
        self.sprtTopBar.y = self.height - self.barHeight
        self.sprtTopBar.scale_x = self.width / self.sprtTopBar.width

        # Initialize the buttons for a new game and settings
        pressedImage = resource.image(f"{self.themeDir}/settings0.png")
        releasedImage = resource.image(f"{self.themeDir}/settings1.png")
        bSize = button_size(self.barHeight)
        bYLoc = (self.height - (self.barHeight) / 2) - bSize / 2
        def btnCommand(): return SettingsWindow(self.save)

        self.btnSettings = GameButton(self.width / 2 - (bSize + 4), bYLoc,
                                    releasedImage, pressedImage, bSize, bSize, btnCommand, self.batch)

        pressedImage = resource.image(f"{self.themeDir}/newGame0.png")
        releasedImage = resource.image(f"{self.themeDir}/newGame1.png")
        self.btnNewGame = GameButton((self.width / 2), bYLoc,
                                    releasedImage, pressedImage, bSize, bSize, self.reset, self.batch)

        self.cntFlags.setCounter(0)
        self.timer.setCounter(0)
        self.timer.locked = True
    
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

    def on_mouse_release(self, x, y, b, m):
        # Get mouse coordinates on the board
        real_tile_size = self.tileSize
        posX = int((x - self.emptySpace[0]) / real_tile_size)
        posY = int((y - self.emptySpace[1]) / real_tile_size)

        # Check if the mouse is in the top bar
        self.btnSettings.clickEvent(x, y, 1)
        self.btnNewGame.clickEvent(x, y, 1)
        if (posX >= 0 and posX < self.gameSize[0]) and (posY >= 0 and posY < self.gameSize[1]):
            # Place a flag on the tile if key 4 is pressed (right click)
            if b == 4:
                self.flagTile(posX, posY)

            elif b == 1:  # Reveal the tile if key 1 is pressed (left click)
                if self.started:  # Check if the game has started and start it if not
                    self.clickTile(posX, posY)
                else:
                    self.startGame(posX, posY)

    def on_mouse_press(self, x, y, b, m):
        self.btnSettings.clickEvent(x, y, 0)
        self.btnNewGame.clickEvent(x, y, 0)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        return
        MAX_ZOOM = 5
        MIN_ZOOM = 1
        xZoomTo = int((x / self.width) * len(self.tiles[0]))
        yZoomTo = int((y / self.height) * len(self.tiles))

        for idy, row in enumerate(self.tiles):
            for idx, tile in enumerate(row):
                pdy = idy - yZoomTo
                pdx = idx - xZoomTo
                oldWidth = tile.width
                oldHeight = tile.height

                tile.scale = min(MAX_ZOOM,
                                max(MIN_ZOOM, tile.scale + (scroll_y))
                                )
                tile.x -= pdx * (oldWidth - tile.width)
                tile.y -= pdy * (oldHeight - tile.height)