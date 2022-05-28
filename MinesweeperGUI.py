from pyglet import *
from random import random
from GameObjects import *


def button_size(h):
    return h / 1.5


class Minesweeper(window.Window):
    def __init__(self, theme="Star Wars 2", difficulty=0.25, gameSize=(10, 10), windowSize=(500, 500)):
        """
        Extends pyglet.window.Window and contains a minesweeper game.
        - theme: The name of the folder that contains the theme to use
        - difficulty: The fraction of tiles that will be bombs, defaults to 0.25, medium
        - gameSize: The width and height of the game given in the nuber of tiles
        - windowSize: The size of the actual window
        """
        super(Minesweeper, self).__init__(
            windowSize[0], windowSize[1], caption="Minesweeper", style='dialog')
        tp = f"Themes/{theme}"

        self.batch = graphics.Batch()

        # Initialize class variables for the game and GUI
        self.tiles = []
        self.difficulty = difficulty
        self.gameSize = gameSize
        self.theme = theme
        self.started = False
        self.gameOver = False

        # Initialize the top bar, and counters for timer and flags
        self.sprtTopBar = sprite.Sprite(resource.image(
            f"Themes/{theme}/TopBar.png"), batch=self.batch)
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
        pImage = resource.image(f"{tp}/settings0.png")
        rImage = resource.image(f"{tp}/settings1.png")
        bSize = button_size(self.barHeight)
        bYLoc = (self.height - (self.barHeight) / 2) - bSize / 2
        def btnCommand(): return SettingsWindow(self.save)

        self.btnSettings = Button(self.width / 2 - (bSize + 4), bYLoc,
                                  rImage, pImage, bSize, bSize, btnCommand, self.batch)

        pImage = resource.image(f"{tp}/newGame0.png")
        rImage = resource.image(f"{tp}/newGame1.png")
        self.btnNewGame = Button((self.width / 2), bYLoc,
                                 rImage, pImage, bSize, bSize, self.reset, self.batch)

        self.cntTimer = Counter(
            self.width / 3, self.height - (self.barHeight / 2), self.batch)

        self.cntFlags = Counter(
            2 * self.width / 3, self.height - (self.barHeight / 2), self.batch)

        # Contains the images for each tile value
        self.themeKey = {0: resource.image(f"{tp}/none.png"),
                         1: resource.image(f"{tp}/one.png"),
                         2: resource.image(f"{tp}/two.png"),
                         3: resource.image(f"{tp}/three.png"),
                         4: resource.image(f"{tp}/four.png"),
                         5: resource.image(f"{tp}/five.png"),
                         6: resource.image(f"{tp}/six.png"),
                         7: resource.image(f"{tp}/seven.png"),
                         8: resource.image(f"{tp}/eight.png"),
                         9: resource.image(f"{tp}/bomb.png"),
                         10: resource.image(f"{tp}/blank.png")}

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
        self.theme = theme
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
            f"Themes/{self.theme}/newGameLost1.png")
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
        self.themeKey = {0: resource.image(f"Themes/{name}/none.png"),
                         1: resource.image(f"Themes/{name}/one.png"),
                         2: resource.image(f"Themes/{name}/two.png"),
                         3: resource.image(f"Themes/{name}/three.png"),
                         4: resource.image(f"Themes/{name}/four.png"),
                         5: resource.image(f"Themes/{name}/five.png"),
                         6: resource.image(f"Themes/{name}/six.png"),
                         7: resource.image(f"Themes/{name}/seven.png"),
                         8: resource.image(f"Themes/{name}/eight.png"),
                         9: resource.image(f"Themes/{name}/bomb.png"),
                         10: resource.image(f"Themes/{name}/blank.png")}

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
            f"Themes/{self.theme}/TopBar.png"), batch=self.batch)
        self.sprtTopBar.y = self.height - self.barHeight
        self.sprtTopBar.scale_x = self.width / self.sprtTopBar.width

        # Initialize the buttons for a new game and settings
        pImage = resource.image(f"Themes/{self.theme}/settings0.png")
        rImage = resource.image(f"Themes/{self.theme}/settings1.png")
        bSize = button_size(self.barHeight)
        bYLoc = (self.height - (self.barHeight) / 2) - bSize / 2
        def btnCommand(): return SettingsWindow(self.save)

        self.btnSettings = Button(self.width / 2 - (bSize + 4), bYLoc,
                                  rImage, pImage, bSize, bSize, btnCommand, self.batch)

        pImage = resource.image(f"Themes/{self.theme}/newGame0.png")
        rImage = resource.image(f"Themes/{self.theme}/newGame1.png")

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
        self.btnNewGame = Button((self.width / 2), bYLoc,
                                 rImage, pImage, bSize, bSize, self.reset, self.batch)

    def clickTile(self, x, y):
        if not(self.gameOver):
            self.autoClear(x, y)
            self.revealTile(x, y)

    def revealTile(self, x, y):
        # Reveals the tile at the given coordinate
        tile = self.tiles[y][x]
        if not(tile.isFlagged) and not(tile.isRevealed):
            tile.isRevealed = True
            tile.image = self.themeKey[tile.value]
            if tile.value == 0:
                self.clearBlanks(x, y)
            elif tile.value == 9:
                tile.image = resource.image(
                    f"Themes/{self.theme}/incorrectBomb.png")
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
            tile.image = resource.image(f"Themes/{self.theme}/flag.png")
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
