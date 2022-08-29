import difflib
from random import random
from src.game.ControlTile import ControlTile
from src.game.utils.TileUtils import TileSet

DEFAULT_DIFF = 0.16
DEFAULT_SIZE = (20, 15)


class MinesweeperMC:
    def __init__(self, gameSize=DEFAULT_SIZE, difficulty=DEFAULT_DIFF):
        self.tiles = TileSet()
        self.difficulty = difficulty
        self.gameSize = gameSize
        self.started = False
        self.gameOver = False

        # Generate unrevealed tiles with no other values as a placeholder until the game is started
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):
                row.append(ControlTile(x, y, y * self.gameSize[0] + x))
            self.tiles.append(row)

    def clickEvent(self, x, y, flag):
        if self.started:
            if flag:
                self.flagTile(x, y)
            else:
                self.revealTile(x, y)
        else:
            self.startGame(x, y)

    def reset(self):
        self.tiles = TileSet()
        self.difficulty = DEFAULT_DIFF
        self.gameSize = DEFAULT_SIZE
        self.started = False
        self.gameOver = False

        # Generate unrevealed tiles with no other values as a placeholder until the game is started
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):
                row.append(ControlTile(x, y, y * self.gameSize[0] + x))
            self.tiles.append(row)

    def revealTile(self, x, y):
        tile = self.tiles.getTileAtCoord(x, y)
        if not (tile.flagged or tile.revealed):
            tile.revealed = True
            if tile.value == 0:
                self.revealAllNearTiles(x, y)
            elif tile.value == 9:
                self.endGame()
        elif not tile.flagged and tile.revealed:
            self.autoClearNearTiles(x, y)

        tile.updated = False

    def flagTile(self, x, y):
        tile = self.tiles.getTileAtCoord(x, y)
        tile.flagged = not tile.flagged
        tile.updated = False

    def generateBombs(self, start_x, start_y):
        self.tiles = TileSet()
        tiles_left = self.gameSize[0] * self.gameSize[1]
        bombs_left = tiles_left * self.difficulty

        # Generate the bombs
        for y in range(self.gameSize[1]):
            row = []
            for x in range(self.gameSize[0]):
                # Do not place any bombs within a radius of one of the clicked position
                # This is done so the start of the game is easier
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

                new_tile = ControlTile(x, y, y * self.gameSize[0] + x, value=value)
                tiles_left -= 1
                row.append(new_tile)
            self.tiles.append(row)

    def generateTileValues(self):
        for y in range(self.gameSize[1]):
            for x in range(self.gameSize[0]):
                currentTile = self.tiles.getTileAtCoord(x, y)
                currentTile.setNearTiles(self.getNearTiles(x, y))
                if currentTile.value is None:
                    bombs_near = 0
                    # The value of each tile that isn't a bomb is equal to the number of bombs adjacent to it
                    for near_tile in currentTile.nearTiles:
                        if near_tile.value == 9:
                            bombs_near += 1
                    currentTile.value = bombs_near

    def generateTiles(self, x, y):
        self.generateBombs(x, y)
        self.generateTileValues()

    def endGame(self):
        self.gameOver = True
        def f(tile):
            if tile.value == 9:
                tile.revealed = True
                tile.updated = False

        self.tiles.forAll(f)

    def startGame(self, x, y):
        self.started = True
        self.generateTiles(x, y)
        self.revealTile(x, y)

    def revealAllNearTiles(self, x, y):
        for tile in self.tiles.getTileAtCoord(x, y).nearTiles:
            self.revealTile(tile.x, tile.y)

    def getNearTiles(self, x, y):
        near_tiles = []
        for px in range(x - 1, x + 2):
            for py in range(y - 1, y + 2):
                if px != x or py != y:
                    if 0 <= px < self.gameSize[0] and 0 <= py < self.gameSize[1]:
                        near_tiles += [self.tiles.getTileAtCoord(px, py)]
        return near_tiles

    def autoClearNearTiles(self, x, y):
        tile = self.tiles.getTileAtCoord(x, y)
        if tile.revealed and tile.getNearFlags() == tile.value:
            for nt in tile.nearTiles:
                if not nt.revealed:
                    self.revealTile(nt.x, nt.y)

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

    def save(self, difficulty, gameSize):
        self.difficulty = difficulty
        self.gameSize = gameSize
