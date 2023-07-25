from pyglet import window, resource, sprite, graphics
from pyglet.window.mouse import LEFT, RIGHT
from src.main.components.Counter import Timer, Counter
from src.main.components.MSButton import Button
from src.main.components.TopBar import TopBar
from src.main.game.MinesweeperModelControl import MinesweeperMC
from src.main.components.ConfigurationWindow import ConfigWindow
from src.main.game.TileSprite import TileSprite
from time import time

class MinesweeperV(window.Window):
    def __init__(self, theme, difficulty, game_size, window_size, dev=False):
        super(MinesweeperV, self).__init__(
            window_size[0], window_size[1], caption="Minesweeper")
        self.minesweeper_control = MinesweeperMC(game_size, difficulty)
        self.theme_dir = theme
        self.theme_key = self.get_theme_key()
        self.batch = graphics.Batch() 
        self.tiles = []
        self.dragging = False
        self.prevTime = 0
        self.mouse_down_time = 0
        self.tile_size = 0
        self.empty_space = []
        self.dev = dev
        if dev:
            self.fps_display = window.FPSDisplay(window=self)

        self.top_bar = TopBar(self, self.theme_dir, self.batch)
        self.btn_settings = Button(self.top_bar, 1, "settings1.png", "settings0.png", self.theme_dir, self.batch, lambda: ConfigWindow(self.save))
        self.btn_newGame = Button(self.top_bar, 0, "newGame1.png", "newGame0.png", self.theme_dir, self.batch, self.reset)
        self.timer = Timer(self.width / 3, self.height - (self.top_bar.getHeight() / 2), self.batch)
        self.timer.locked = True
        self.cntFlags = Counter(2 * self.width / 3, self.height - (self.top_bar.getHeight() / 2), self.batch)

        self.calculate_tile_size()
        self.zoom_minmax = [0, self.tile_size]
        self.calculate_empty_space()

        self.generate_blank_tiles()
        self.grid_size = [len(self.tiles[0]) * self.tile_size, len(self.tiles) * self.tile_size]

    def generate_blank_tiles(self):
        for y in range(self.minesweeper_control.game_size[1]):
            row = []
            for x in range(self.minesweeper_control.game_size[0]):
                x_pos = x * self.tile_size + self.empty_space[0]
                y_pos = y * self.tile_size + self.empty_space[1]
                row.append(TileSprite(x_pos, y_pos, self.tile_size, self.theme_key[10], self.batch))
            self.tiles.append(row)

    def calculate_empty_space(self):
        self.empty_space = [
            (self.width - (self.minesweeper_control.game_size[0] * self.tile_size)) / 2,
            (self.height - self.top_bar.getHeight() -
             (self.minesweeper_control.game_size[1] * self.tile_size)) / 2
        ]

    def calculate_tile_size(self):
        self.tile_size = min(self.width // self.minesweeper_control.game_size[0],
                            (self.height - self.top_bar.getHeight()) // self.minesweeper_control.game_size[1])

    def set_theme(self, name):
        self.theme_dir = name
        self.theme_key = self.get_theme_key()

    def update(self):
        self.cntFlags.setCounter(self.minesweeper_control.tiles.getFlaggedCount())
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                self.update_tile(tile, self.minesweeper_control.tiles[y][x])
        self.timer.locked = self.minesweeper_control.game_over or not self.minesweeper_control.started

    def update_tile(self, update_tile, ref_tile):
        if ref_tile.updated:
            return
        if ref_tile.flagged:
            update_tile.image = self.theme_key[-1]
        else:
            if ref_tile.revealed:
                update_tile.image = self.theme_key[ref_tile.value]
            else:
                update_tile.image = self.theme_key[10]
        ref_tile.updated = True

    def get_theme_key(self):
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
            d[key] = resource.image(f"{self.theme_dir}/{d[key]}")
        return d

    def save(self, theme, difficulty, game_size, window_size):
        self.minesweeper_control.save(difficulty, game_size)
        self.theme_dir = theme
        self.set_theme(theme)
        self.width, self.height = window_size[0], window_size[1]
        self.reset()

    def zoom(self, x, y, amount):
        x_index, y_index = (x - self.empty_space[0]), (y - self.empty_space[1])
        tile = self.tiles[0][0]
        old_size = self.tile_size
        tile.scale += amount
        current_size = self.tiles[0][0].width
        size_diff = old_size - current_size

        tile.y += size_diff * (y_index - tile.y) // current_size
        tile.x += size_diff * (x_index - tile.x) // current_size

        for index1, row in enumerate(self.tiles):
            for index2, t in enumerate(row):
                if index1 == 0 and index2 == 0:
                    continue
                t.scale += amount
                t.y = index1 * current_size + tile.y
                t.x = index2 * current_size + tile.x
        self.tile_size = self.tiles[0][0].width
        self.update_empty_space()

    def reset(self):
        self.tiles = []
        self.minesweeper_control.reset()

        self.top_bar = TopBar(self, self.theme_dir, self.batch)
        self.btn_settings = Button(self.top_bar, 1, "settings1.png", "settings0.png", self.theme_dir, self.batch, lambda: ConfigWindow(self.save))
        self.btn_newGame = Button(self.top_bar, 0, "newGame1.png", "newGame0.png", self.theme_dir, self.batch, self.reset)

        self.timer.setCounter(0)
        self.cntFlags.setCounter(0)
        self.cntFlags.text = "0"
        self.timer.position = (self.width / 3, self.height - (self.top_bar.getHeight() / 2))
        self.cntFlags.position = (2 * self.width / 3, self.height - (self.top_bar.getHeight() / 2))

        self.calculate_tile_size()
        self.zoom_minmax = [0, self.tile_size]
        self.calculate_empty_space()

        self.generate_blank_tiles()
        self.batch.invalidate()

    def is_click_on_tiles(self, clickX, clickY):
        x_min = self.empty_space[0]
        y_min = self.empty_space[1]
        x_max = self.minesweeper_control.game_size[0] * self.tile_size + self.empty_space[0]
        y_max = self.minesweeper_control.game_size[1] * self.tile_size + self.empty_space[1]
        return x_min < clickX < x_max and y_min < clickY < y_max

    def on_draw(self):
        self.clear()
        self.batch.draw()
        if self.dev:
            self.fps_display.draw()

    def move_tiles_abs(self, x, y):
        for ri, row in enumerate(self.tiles):
            for ti, tile in enumerate(row):
                tile.x = x + ti * self.tile_size
                tile.y = y + ri * self.tile_size

    def on_mouse_release(self, x, y, button, _1):
        if self.dragging:
            self.dragging = False
            return
        # Get mouse coordinates on the board
        x_pos, y_pos = int((x - self.empty_space[0]) / self.tile_size), int((y - self.empty_space[1]) / self.tile_size)

        # Check if the mouse is in the top bar
        self.btn_settings.click_event(x, y, 1)
        self.btn_newGame.click_event(x, y, 1)
        if self.is_click_on_tiles(x, y):
            if button == RIGHT:
                self.minesweeper_control.click_event(x_pos, y_pos, True)
            elif button == LEFT:
                self.minesweeper_control.click_event(x_pos, y_pos, False)
        self.update()

    def on_mouse_press(self, x, y, _, _1):
        self.mouse_down_time = time()
        self.btn_settings.click_event(x, y, 0)
        self.btn_newGame.click_event(x, y, 0)

    def on_mouse_drag(self, x, y, dx, dy, _, _1):
        # if the mouse has not moved far, or we have not been dragging for long, do not drag
        move_threshold = 5
        time_threshold = 0.2
        if (abs(dx) < move_threshold and abs(dy) < move_threshold) and (time() - self.mouse_down_time < time_threshold):
            return
        self.dragging = True
        x_min, y_min = self.empty_space[0] + dx, self.empty_space[1] + dy
        x_max = self.minesweeper_control.game_size[0] * self.tile_size + self.empty_space[0] + dx
        y_max = self.minesweeper_control.game_size[1] * self.tile_size + self.empty_space[1] + dy
        if x_min > 0:
            dx -= x_min
        elif x_max < self.width:
            dx += self.width - x_max
        if y_min > 0:
            dy -= y_min
        elif y_max < self.height - self.top_bar.getHeight():
            dy += self.height - self.top_bar.getHeight() - y_max
        self.empty_space[0] += dx
        self.empty_space[1] += dy
        self.move_tiles_abs(self.empty_space[0], self.empty_space[1])
        
    def on_mouse_scroll(self, x, y, dx, dy):
        new_scale = dy * self.tile_size / 200
        self.zoom(x, y, new_scale)
        self.grid_size = [len(self.tiles[0]) * self.tile_size, len(self.tiles) * self.tile_size]

    def update_empty_space(self):
        ref_tile = self.tiles[0][0]
        self.empty_space[0] = ref_tile.x
        self.empty_space[1] = ref_tile.y
