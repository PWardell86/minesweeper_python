from pyglet import window, resource, sprite, graphics

from src.main.components.Counter import Timer, Counter
from src.main.components.MSButton import Button
from src.main.components.TopBar import TopBar
from src.main.game.MinesweeperModelControl import MinesweeperMC
from src.main.components.ConfigurationWindow import ConfigWindow
from src.main.game.TileSprite import TileSprite
from time import time

def getButtonSize(h):
    return h / 1.5


class MinesweeperV(window.Window):
    def __init__(self, theme="Default", difficulty=0.25, gameSize=(10, 10), windowSize=(500, 500), dev=False):
        # TODO: Clean up this initialization
        super(MinesweeperV, self).__init__(
            windowSize[0], windowSize[1], caption="Minesweeper")
        self.minesweeperControl = MinesweeperMC(gameSize, difficulty)
        self.themeDir = theme
        self.batch = graphics.Batch()
        self.tiles = []  # A 2D list indexed by (y, x)
        self.dragging = False
        self.prevTime = 0
        self.mouse_down_time = 0
        self.dev = dev
        if self.dev:
            self.fps_display = window.FPSDisplay(window=self)

        # TODO: Refactor the top bar into a separate class
        # Initialize the top bar, and counters for timer and flags
        self.sprtTopBar = sprite.Sprite(resource.image(
            f"{self.themeDir}/TopBar.png"), batch=self.batch, group=graphics.OrderedGroup(1))
        self.barHeight = self.sprtTopBar.height
        self.sprtTopBar.y = self.height - self.barHeight
        self.sprtTopBar.scale_x = self.width / self.sprtTopBar.width

        self.tileSize = min(windowSize[0] // gameSize[0], (windowSize[1] - self.barHeight) // gameSize[1])
        self.zoom_minmax = [0, self.tileSize]

        self.emptySpace = [
            (self.width - (gameSize[0] * self.tileSize)) / 2,
            (self.height - self.barHeight -
             (gameSize[1] * self.tileSize)) / 2
        ]

        # TODO: Refactor the button initialization into a new class
        # Initialize the buttons for a new main and settings
        pressed_img = resource.image(f"{self.themeDir}/settings0.png")
        unpressed_img = resource.image(f"{self.themeDir}/settings1.png")
        btn_size = getButtonSize(self.barHeight)
        y_offset = (self.height - self.barHeight / 2) - btn_size / 2

        self.btnSettings = Button(self.width / 2 - (btn_size + 4), y_offset,
                                  unpressed_img, pressed_img, btn_size, btn_size,
                                  self.batch, lambda: ConfigWindow(self.save))

        pressed_img = resource.image(f"{self.themeDir}/newGame0.png")
        unpressed_img = resource.image(f"{self.themeDir}/newGame1.png")
        self.btnNewGame = Button((self.width / 2), y_offset,
                                 unpressed_img, pressed_img, btn_size, btn_size, self.batch, self.reset)

        self.timer = Timer(
            self.width / 3, self.height - (self.barHeight / 2), self.batch)
        self.timer.locked = True
        self.cntFlags = Counter(
            2 * self.width / 3, self.height - (self.barHeight / 2), self.batch)

        # Contains the images for each tile value
        self.themeKey = self.getThemeKey()

        # Generate unrevealed tiles with no other values as a placeholder until the main is started
        for y in range(gameSize[1]):
            row = []
            for x in range(gameSize[0]):
                x_pos = x * self.tileSize + self.emptySpace[0]
                y_pos = y * self.tileSize + self.emptySpace[1]
                row.append(TileSprite(x_pos, y_pos, self.tileSize, self.themeKey[10], self.batch))
            self.tiles.append(row)

        self.gridSize = [len(self.tiles[0]) * self.tileSize, len(self.tiles) * self.tileSize]

    def setTheme(self, name):
        """
        Updates the theme of the main to the given folder, name
        """
        # Set the theme of the main theme folder
        self.themeDir = name
        self.themeKey = self.getThemeKey()

    def update(self):
        self.cntFlags.setCounter(self.minesweeperControl.tiles.getFlaggedCount())
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                self.update_tile(tile, self.minesweeperControl.tiles[y][x])
        self.timer.locked = self.minesweeperControl.gameOver or not self.minesweeperControl.started

    def update_tile(self, tile, reference_tile):
        """
        Updates the tile at the given coordinates to the reference tile's state
        """
        if reference_tile.updated:
            return
        if reference_tile.flagged:
            tile.image = self.themeKey[-1]
        else:
            if reference_tile.revealed:
                tile.image = self.themeKey[reference_tile.value]
            else:
                tile.image = self.themeKey[10]
        reference_tile.updated = True

    def getThemeKey(self):
        d = {-1: "flag.png",
             0: "none.png",
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

    def save(self, theme, difficulty, gameSize, windowSize):
        self.minesweeperControl.save(difficulty, gameSize)
        self.themeDir = theme
        self.setTheme(theme)
        self.width = windowSize[0]
        self.height = windowSize[1]
        self.reset()

    def zoom(self, x, y, amount):
        xIndex = (x - self.emptySpace[0])
        yIndex = (y - self.emptySpace[1])

        # Move the tile in the bottom_corner and build all tiles off of that
        tile = self.tiles[0][0]

        oldSize = self.tileSize
        tile.scale += amount
        currentSize = self.tiles[0][0].width
        sizeDifference = oldSize - currentSize

        tile.y += sizeDifference * (yIndex - tile.y) // currentSize
        tile.x += sizeDifference * (xIndex - tile.x) // currentSize

        for index1, row in enumerate(self.tiles):
            for index2, t in enumerate(row):
                if index1 == 0 and index2 == 0:
                    continue
                t.scale += amount
                t.y = index1 * currentSize + tile.y
                t.x = index2 * currentSize + tile.x
        self.tileSize = self.tiles[0][0].width
        self.update_empty_space()

    def reset(self):
        """
        Resets the main to its initial state with all class variables
        """

        for row in self.tiles:
            for tile in row:
                tile.delete()
        self.tiles = []
        self.minesweeperControl.reset()

        self.tileSize = min(
            self.width // self.minesweeperControl.gameSize[0], (self.height - self.barHeight) // self.minesweeperControl.gameSize[1])
        self.emptySpace = [
            (self.width - (self.minesweeperControl.gameSize[0] * self.tileSize)) / 2,
            (self.height - self.barHeight -
             (self.minesweeperControl.gameSize[1] * self.tileSize)) / 2
        ]

        self.sprtTopBar = sprite.Sprite(
            resource.image(f"{self.themeDir}/TopBar.png"), batch=self.batch, group=graphics.OrderedGroup(1))
        self.sprtTopBar.y = self.height - self.barHeight
        self.sprtTopBar.scale_x = self.width / self.sprtTopBar.width

        # Initialize the buttons for a new main and settings
        pressed_img = resource.image(f"{self.themeDir}/settings0.png")
        unpressed_img = resource.image(f"{self.themeDir}/settings1.png")
        button_size = getButtonSize(self.barHeight)
        y_offset = (self.height - self.barHeight / 2) - button_size / 2

        self.btnSettings = Button(self.width / 2 - (button_size + 4), y_offset,
                                  unpressed_img, pressed_img, button_size, button_size,
                                  self.batch, lambda: ConfigWindow(self.save))

        pressed_img = resource.image(f"{self.themeDir}/newGame0.png")
        unpressed_img = resource.image(f"{self.themeDir}/newGame1.png")
        self.btnNewGame = Button((self.width / 2), y_offset,
                                 unpressed_img, pressed_img, button_size, button_size, self.batch, self.reset)

        self.timer.setCounter(0)
        self.cntFlags.setCounter(0)
        self.cntFlags.text = "0"
        self.timer.x = self.width / 3
        self.timer.y = self.height - (self.barHeight / 2)
        self.cntFlags.x = 2 * self.width / 3
        self.cntFlags.y = self.height - (self.barHeight / 2)

        for y in range(self.minesweeperControl.gameSize[1]):
            row = []
            for x in range(self.minesweeperControl.gameSize[0]):
                x_pos = x * self.tileSize + self.emptySpace[0]
                y_pos = y * self.tileSize + self.emptySpace[1]
                row.append(TileSprite(x_pos, y_pos, self.tileSize, self.themeKey[10], self.batch))
            self.tiles.append(row)
        self.batch.invalidate()

    def isMouseClickWithinGameBounds(self, clickX, clickY):
        x_min = self.emptySpace[0]
        y_min = self.emptySpace[1]
        x_max = self.minesweeperControl.gameSize[0] * self.tileSize + self.emptySpace[0]
        y_max = self.minesweeperControl.gameSize[1] * self.tileSize + self.emptySpace[1]
        return x_min < clickX < x_max and y_min < clickY < y_max

    def on_draw(self):
        self.clear()
        self.batch.draw()
        if self.dev:
            self.fps_display.draw()

    def move_tiles_abs(self, x, y):
        for ri, row in enumerate(self.tiles):
            for ti, tile in enumerate(row):
                tile.x = x + ti * self.tileSize
                tile.y = y + ri * self.tileSize

    def on_mouse_release(self, x, y, button, _1):
        if self.dragging:
            self.dragging = False
            return
        # Get mouse coordinates on the board
        x_pos = int((x - self.emptySpace[0]) / self.tileSize)
        y_pos = int((y - self.emptySpace[1]) / self.tileSize)

        # Check if the mouse is in the top bar
        self.btnSettings.clickEvent(x, y, 1)
        self.btnNewGame.clickEvent(x, y, 1)
        if self.isMouseClickWithinGameBounds(x, y):
            # Place a flag on the tile if key 4 is pressed (right click)
            if button == 4:
                self.minesweeperControl.clickEvent(x_pos, y_pos, True)
            elif button == 1:  # Reveal the tile if key 1 is pressed (left click)
                self.minesweeperControl.clickEvent(x_pos, y_pos, False)
        self.update()

    def on_mouse_press(self, x, y, _, _1):
        self.mouse_down_time = time()
        self.btnSettings.clickEvent(x, y, 0)
        self.btnNewGame.clickEvent(x, y, 0)

    def on_mouse_drag(self, x, y, dx, dy, _, _1):
        # if the mouse has not moved far, or we have not been dragging for long, do not drag
        move_threshold = 5
        time_threshold = 0.2
        if (abs(dx) < move_threshold and abs(dy) < move_threshold) and (time() - self.mouse_down_time < time_threshold):
            return
        self.dragging = True
        x_min = self.emptySpace[0] + dx
        y_min = self.emptySpace[1] + dy
        x_max = self.minesweeperControl.gameSize[0] * self.tileSize + self.emptySpace[0] + dx
        y_max = self.minesweeperControl.gameSize[1] * self.tileSize + self.emptySpace[1] + dy
        if x_min > 0:
            dx -= x_min
        if x_max < self.width:
            dx += self.width - x_max
        if y_min > 0:
            dy -= y_min
        if y_max < self.height - self.barHeight:
            dy += self.height - self.barHeight - y_max
        self.emptySpace[0] += dx
        self.emptySpace[1] += dy
        self.move_tiles_abs(self.emptySpace[0], self.emptySpace[1])
        

    def on_mouse_scroll(self, x, y, dx, dy):
        newScale = dy * self.tileSize / 200
        self.zoom(x, y, newScale)
        self.gridSize = [len(self.tiles[0]) * self.tileSize, len(self.tiles) * self.tileSize]

    def update_empty_space(self):
        cornerTile = self.tiles[0][0]
        self.emptySpace[0] = cornerTile.x
        self.emptySpace[1] = cornerTile.y
