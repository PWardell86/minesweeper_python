from pyglet import *
from random import random
from os import path

from src.game.Counter import Timer, Counter
from src.game.GameButton import GameButton
from src.game.SettingsWindow import SettingsWindow
from src.game.Tile import Tile

working_dir = path.dirname(path.realpath(__file__))
resource.path = [working_dir, path.realpath('../resources')]
print(resource.path)


def getButtonSize(h):
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
        self.dragging = False
        self.resetting = False


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
        pressed_img = resource.image(f"{self.themeDir}/settings0.png")
        unpressed_img = resource.image(f"{self.themeDir}/settings1.png")
        btn_size = getButtonSize(self.barHeight)
        y_offset = (self.height - self.barHeight / 2) - btn_size / 2

        self.btnSettings = GameButton(self.width / 2 - (btn_size + 4), y_offset,
                                      unpressed_img, pressed_img, btn_size, btn_size,
                                      lambda: SettingsWindow(self.save), self.batch)

        pressed_img = resource.image(f"{self.themeDir}/newGame0.png")
        unpressed_img = resource.image(f"{self.themeDir}/newGame1.png")
        self.btnNewGame = GameButton((self.width / 2), y_offset,
                                     unpressed_img, pressed_img, btn_size, btn_size, self.reset, self.batch)

        self.timer = Timer(
            self.width / 3, self.height - (self.barHeight / 2), self.batch)

        self.cntFlags = Counter(
            2 * self.width / 3, self.height - (self.barHeight / 2), self.batch)

        self.timer.locked = True
        # Contains the images for each tile value
        self.themeKey = self.getThemeKey()

        # Generate unrevealed tiles with no other values as a placeholder until the game is started
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):
                row.append(Tile(x * self.tileSize + self.emptySpace[0], y * self.tileSize + self.emptySpace[1],
                                self.tileSize, (x, y), self.themeKey[10],
                                self.batch, None))
            self.tiles.append(row)

    def generateTiles(self, start_x, start_y):
        self.calculateBombTiles(start_x, start_y)
        self.calculateTileValues()

    def calculateBombTiles(self, start_x, start_y):

        self.tiles = []
        tiles_left = self.gameSize[0] * self.gameSize[1]
        bombs_left = tiles_left * self.difficulty

        # Generate the bombs
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):
                # Do not place any bombs within a radius of one of the clicked position
                # This is done so the start of the game is easier
                dx = abs(x - start_x)
                dy = abs(y - start_y)
                value = None
                if dx > 1 or dy > 1:
                    # The chance of a tile being a bomb is equal to:
                    # The number of bombs left to place divided by the number of tiles left to look over
                    bomb_chance = bombs_left / tiles_left
                    if bomb_chance >= random():
                        value = 9
                        bombs_left -= 1

                new_tile = Tile(x * self.tileSize + self.emptySpace[0], y * self.tileSize + self.emptySpace[1],
                                self.tileSize, (x, y), self.themeKey[10],
                                self.batch, value=value)
                tiles_left -= 1
                row.append(new_tile)
            self.tiles.append(row)

    def calculateTileValues(self):
        for y in range(self.gameSize[1]):
            for x in range(self.gameSize[0]):
                if self.tiles[y][x].value is None:
                    bombs_near = 0
                    self.tiles[y][x].setNearTiles(self.getNearTiles(x, y))
                    # The value of each tile that isnt a bomb is equal to the number of bombs adjacent to it
                    for near_tile in self.tiles[y][x].nearTiles:
                        if near_tile.value == 9:
                            bombs_near += 1
                    self.tiles[y][x].value = bombs_near

    def setTheme(self, name):
        """
        Updates the theme of the game to the given folder, name
        """
        # Set the theme of the game theme folder
        self.themeDir = name
        self.themeKey = self.getThemeKey()

    def startGame(self, start_x, start_y):
        """
        Starts the game at the given tile coordinate
        """
        self.started = True
        self.timer.locked = False
        self.cntFlags.locked = False
        self.generateTiles(start_x, start_y)
        self.revealTile(start_x, start_y)

    def endGame(self):
        """
        Ends the game. Resets the timer, flag count, score and board.
        """
        self.btnNewGame.image = resource.image(
            f"{self.themeDir}/newGameLost1.png")
        self.gameOver = True
        self.timer.locked = True
        for row in self.tiles:
            for tile in row:
                if tile.value == 9:
                    if not tile.isRevealed:
                        tile.image = self.themeKey[9]

    def clickTile(self, x, y):
        if not self.gameOver:
            self.autoClear(x, y)
            self.revealTile(x, y)

    def revealTile(self, x: int, y: int):
        """Reveals the tile at the given coordinate"""
        tile = self.tiles[y][x]
        if not (tile.isFlagged or tile.isRevealed):
            tile.isRevealed = True
            tile.image = self.themeKey[tile.value]
            if tile.value == 0:
                self.clearBlanks(x, y)
            elif tile.value == 9:
                tile.image = resource.image(
                    f"{self.themeDir}/incorrectBomb.png")
                self.endGame()

    def revealTileFromTile(self, tile):
        self.revealTile(tile.index[0], tile.index[1])

    def flagTile(self, x, y):
        """
        Toggles whether the tile at the tile coordinates is flagged or not
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

    def flagTileFromTile(self, tile):
        self.flagTile(tile.index[0], tile.index[1])

    def clearBlanks(self, x, y):
        """
        Recursively reveals all tiles surrounding a blank tile
        """
        # Clears the blanks around the revealed tile
        for px in range(x - 1, x + 2):
            for py in range(y - 1, y + 2):
                if px != x or py != y:
                    if 0 <= px < self.gameSize[0] and 0 <= py < self.gameSize[1]:
                        self.revealTile(px, py)

    def autoClear(self, x, y):
        """
        If all the bombs around a revealed tile are flagged, this will reveal the rest of the tiles
        """
        tile = self.tiles[y][x]
        if tile.isRevealed:
            flag_count = 0
            for near_tile in tile.nearTiles:
                if near_tile.isFlagged:
                    flag_count += 1
            if flag_count == tile.value:
                for px in range(x - 1, x + 2):
                    for py in range(y - 1, y + 2):
                        if px != x or py != y:
                            if 0 <= px < self.gameSize[0] and 0 <= py < self.gameSize[1]:
                                self.revealTile(px, py)

    def getNearTiles(self, x, y):
        """
        Returns all tiles adjacent to the tile at [y][x] in self.tiles
        - Can return 4, 6, or 9 tiles
        """
        near_tiles = []
        for px in range(x - 1, x + 2):
            for py in range(y - 1, y + 2):
                if px != x or py != y:
                    if 0 <= px < self.gameSize[0] and 0 <= py < self.gameSize[1]:
                        near_tiles += [self.tiles[py][px]]
        return near_tiles

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

    def save(self, theme, difficulty, game_size, window_size):
        self.themeDir = theme
        self.setTheme(theme)
        self.difficulty = difficulty
        self.gameSize = game_size
        self.width = window_size[0]
        self.height = window_size[1]
        self.reset()

    def reset(self):
        self.resetting = True
        self.resetGame()
        self.resetting = False

    def resetGame(self):
        """
        Resets the game to its initial state with all class variables
        """
        # Resets the game
        self.started = False
        self.gameOver = False
        for row in self.tiles:
            for tile in row:
                tile.delete()
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
        pressed_img = resource.image(f"{self.themeDir}/settings0.png")
        unpressed_img = resource.image(f"{self.themeDir}/settings1.png")
        button_size = getButtonSize(self.barHeight)
        y_offset = (self.height - self.barHeight / 2) - button_size / 2

        self.btnSettings = GameButton(self.width / 2 - (button_size + 4), y_offset,
                                      unpressed_img, pressed_img, button_size, button_size,
                                      lambda: SettingsWindow(self.save), self.batch)

        pressed_img = resource.image(f"{self.themeDir}/newGame0.png")
        unpressed_img = resource.image(f"{self.themeDir}/newGame1.png")
        self.btnNewGame = GameButton((self.width / 2), y_offset,
                                     unpressed_img, pressed_img, button_size, button_size, self.reset, self.batch)

        self.timer.setCounter(0)
        self.cntFlags.setCounter(0)
        self.cntFlags.text = "0"
        self.timer.x = self.width / 3
        self.timer.y = self.height - (self.barHeight / 2)
        self.cntFlags.x = 2 * self.width / 3
        self.cntFlags.y = self.height - (self.barHeight / 2)
        self.timer.locked = True

        for x in range(self.gameSize[0]):
            row = []
            for y in range(self.gameSize[1]):
                row.append(Tile(x * self.tileSize + self.emptySpace[0], y * self.tileSize + self.emptySpace[1],
                                self.tileSize, (x, y), self.themeKey[10],
                                self.batch, None))
            self.tiles.append(row)
        self.batch.invalidate()

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragging:
            self.dragging = False
            return
        # Get mouse coordinates on the board
        x_pos = int((x - self.emptySpace[0]) / self.tileSize)
        y_pos = int((y - self.emptySpace[1]) / self.tileSize)

        # Check if the mouse is in the top bar
        self.btnSettings.clickEvent(x, y, 1)
        self.btnNewGame.clickEvent(x, y, 1)
        if 0 <= x_pos < self.gameSize[0] and 0 <= y_pos < self.gameSize[1]:
            # Place a flag on the tile if key 4 is pressed (right click)
            if button == 4:
                self.flagTile(x_pos, y_pos)

            elif button == 1:  # Reveal the tile if key 1 is pressed (left click)
                if self.started:  # Check if the game has started and start it if not
                    self.clickTile(x_pos, y_pos)
                else:
                    self.startGame(x_pos, y_pos)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.btnSettings.clickEvent(x, y, 0)
        self.btnNewGame.clickEvent(x, y, 0)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.dragging = True
        for row in self.tiles:
            for tile in row:
                tile.x += dx
                tile.y += dy
        self.update_empty_space()

    def on_mouse_scroll(self, x, y, dx, dy):
        # There is never a time when we want to scale tiles differently, so...
        newScale = dy * 0.05
        xIndex = (x - self.emptySpace[0])
        yIndex = (y - self.emptySpace[1])

        # Move the tile in the bottom_corner and build all tiles off of that
        tile = self.tiles[0][0]

        oldSize = self.tileSize
        tile.scale += newScale
        currentSize = self.tiles[0][0].width
        sizeDifference = oldSize - currentSize

        tile.y += sizeDifference * (yIndex - tile.y) / currentSize
        tile.x += sizeDifference * (xIndex - tile.x) / currentSize

        for index1, row in enumerate(self.tiles):
            for index2, t in enumerate(row):
                if index1 == 0 and index2 == 0:
                    continue
                t.scale += newScale
                t.y = index1 * currentSize + tile.y
                t.x = index2 * currentSize + tile.x
        self.tileSize = self.tiles[0][0].width
        self.emptySpace[0] = self.tiles[0][0].x
        self.emptySpace[1] = self.tiles[0][0].y

    def update_empty_space(self):
        cornerTile = self.tiles[0][0]
        self.emptySpace[0] = cornerTile.x
        self.emptySpace[1] = cornerTile.y
