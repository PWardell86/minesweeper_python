from random import random

from main.components.ControlTile import ControlTile
from main.utils.TileUtils import TileSet


class MinesweeperMC:
    def __init__(self, game_size, difficulty):
        self.tiles = TileSet()
        self.difficulty = difficulty
        self.game_size = game_size
        self.started = False
        self.game_over = False
        self.total_bombs = int(game_size[0] * game_size[1] * difficulty)
        self.remaining_flags = self.total_bombs
        self.revealed_tile_count = 0

        # Generate unrevealed tiles with no other values as a placeholder until the main is started
        for y in range(self.game_size[1]):
            row = []
            for x in range(self.game_size[0]):
                row.append(ControlTile(x, y, y * self.game_size[0] + x))
            self.tiles.append(row)


    def click_event(self, x, y, flag):
        if self.started and not self.game_over:
            self.check_win()
            if flag:
                self.flag_tile(x, y)
            else:
                self.reveal_tile(x, y)
        else:
            self.start_game(x, y)

    def check_win(self):
        total_tiles = self.game_size[0] * self.game_size[1]
        
        if self.remaining_flags == 0 and self.revealed_tile_count + self.total_bombs == total_tiles:
            self.game_over = True

    def reset(self):
        self.tiles = TileSet()
        self.started = False
        self.game_over = False

        # Generate unrevealed tiles with no other values as a placeholder until the main is started
        for y in range(self.game_size[1]):
            row = []
            for x in range(self.game_size[0]):
                row.append(ControlTile(x, y, y * self.game_size[0] + x))
            self.tiles.append(row)

    def reveal_tile(self, x, y):
        tile = self.tiles.getTileAtCoord(x, y)
        if not (tile.flagged or tile.revealed):
            tile.revealed = True
            tile.updated = False
            self.revealed_tile_count += 1
            if tile.value == 0:
                return self.reveal_all_near_tiles(x, y)
            if tile.is_bomb():
                self.end_game()
                return False
        elif not tile.flagged and tile.revealed:
            tile.updated = False
            return self.auto_clear_near_tiles(x, y)

        return False

    def flag_tile(self, x, y):
        tile = self.tiles.getTileAtCoord(x, y)
        self.remaining_flags += 1 if tile.flagged else -1

        if not tile.revealed:
            tile.flagged = not tile.flagged
            tile.updated = False

    def generate_bombs(self, start_x, start_y):
        self.tiles = TileSet()
        tiles_left = self.game_size[0] * self.game_size[1]
        bombs_left = int(tiles_left * self.difficulty)

        # Generate the bombs
        for y in range(self.game_size[1]):
            row = []
            for x in range(self.game_size[0]):
                # Do not place any bombs within a radius of one of the clicked position
                # This is done so the start of the main is easier
                dx = abs(start_x - x)
                dy = abs(start_y - y)
                value = None
                if dx > 1 or dy > 1:
                    # The chance of a tile being a bomb is equal to:
                    # The number of bombs left to place divided by the number of tiles left to look over
                    bomb_chance = bombs_left / tiles_left
                    if bomb_chance >= random():
                        value = 9
                        bombs_left -= 1

                new_tile = ControlTile(x, y, y * self.game_size[0] + x, value=value)
                tiles_left -= 1
                row.append(new_tile)
            self.tiles.append(row)

    def generate_tile_values(self):
        for y in range(self.game_size[1]):
            for x in range(self.game_size[0]):
                current_tile = self.tiles.getTileAtCoord(x, y)
                current_tile.set_near_tiles(self.get_near_tiles(x, y))
                if current_tile.value is None:
                    bombs_near = 0
                    # The value of each tile that isn't a bomb is equal to the number of bombs adjacent to it
                    for near_tile in current_tile.near_tiles:
                        if near_tile.value == 9:
                            bombs_near += 1
                    current_tile.value = bombs_near

    def generate_tiles(self, x, y):
        self.generate_bombs(x, y)
        self.generate_tile_values()

    def end_game(self):
        self.game_over = True

        def f(tile):
            if tile.value == 9:
                tile.revealed = True
                tile.updated = False

        self.tiles.forAll(f)

    def start_game(self, x, y):
        self.started = True
        self.generate_tiles(x, y)
        self.reveal_tile(x, y)

    def reveal_all_near_tiles(self, x, y):
        output = False
        for tile in self.tiles.getTileAtCoord(x, y).near_tiles:
            output |= self.reveal_tile(tile.x, tile.y)
        return output

    def get_near_tiles(self, x, y):
        near_tiles = []
        for px in range(x - 1, x + 2):
            for py in range(y - 1, y + 2):
                if px != x or py != y:
                    if 0 <= px < self.game_size[0] and 0 <= py < self.game_size[1]:
                        near_tiles += [self.tiles.getTileAtCoord(px, py)]
        return near_tiles

    def auto_clear_near_tiles(self, x, y):
        output = False
        tile = self.tiles.getTileAtCoord(x, y)
        if tile.revealed and tile.get_near_flags() == tile.value:
            for nt in tile.near_tiles:
                if not nt.revealed:
                    output |= self.reveal_tile(nt.x, nt.y)
        return output

    def pretty(self):
        output = ""
        for row in self.tiles:
            for tile in row:
                if not tile.revealed:
                    if tile.flagged:
                        output += " * "
                    else:
                        output += " - "
                else:
                    output += f" {tile.value} "
            output += "\n"
        return output

    def save(self, difficulty, game_size):
        self.difficulty = difficulty
        self.game_size = game_size

    def for_tiles(self, inner_func):
        for row in self.tiles:
            for tile in row:
                inner_func(tile)
