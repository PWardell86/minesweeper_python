from src.game.MinesweeperMVC import Minesweeper
from time import sleep


class SimpleBot:
    def __init__(self, game: Minesweeper):
        self.game = game
        # A list of methods for each special case
        # Must be methods that take no input
        self.specialCases = [
            self.revealAllTiles
            , self.flagAllTiles
        ]

    def start(self):
        self.game.startGame(self.game.gameSize[0] // 2, self.game.gameSize[1] // 2)

    def tick(self, t):
        didSomething = False
        for case in self.specialCases:
            didSomething |= case()
        if didSomething:
            print("Still solving...")
        else:
            print("Done solving...")

    def flagAllTiles(self):
        didSomething = False
        for x in range(self.game.gameSize[0]):
            for y in range(self.game.gameSize[1]):
                tile = self.game.tiles[y][x]
                if tile.isRevealed:
                    didSomething |= self.flagNearTilesIfPossible(tile.nearTiles, tile)

        return didSomething

    def flagNearTilesIfPossible(self, tiles: list, tile):
        didSomething = False
        unrevealedTiles = 0
        flaggedTiles = 0
        otherTiles = []
        for t in tiles:
            if not t.isRevealed and not t.isFlagged:
                unrevealedTiles += 1
            elif t.isFlagged:
                flaggedTiles += 1
            else:
                otherTiles.append(t)
        if unrevealedTiles == tile.value - flaggedTiles:
            for t in otherTiles:
                ix = (t.x - self.game.emptySpace[0]) // self.game.tileSize
                iy = (t.y - self.game.emptySpace[1]) // self.game.tileSize
                self.game.flagTile(int(ix), int(iy))
                didSomething = True
        return didSomething

    def revealAllTiles(self):
        didSomething = False
        for x in range(self.game.gameSize[0]):
            for y in range(self.game.gameSize[1]):
                tile = self.game.tiles[y][x]
                if tile.isRevealed:
                    didSomething |= self.revealNearTilesIfPossible(tile.nearTiles, tile)

        return didSomething

    def revealNearTilesIfPossible(self, tiles: list, tile):
        didSomething = False
        flaggedTiles = 0
        otherTiles = []
        for t in tiles:
            if t.isFlagged:
                flaggedTiles += 1
            elif t.value == 0:
                ix = (t.x - self.game.emptySpace[0]) // self.game.tileSize
                iy = (t.y - self.game.emptySpace[1]) // self.game.tileSize
                self.game.revealTile(int(ix), int(iy))
                didSomething = True
            else:
                otherTiles.append(t)
        if flaggedTiles == tile.value and tile.value != 0:
            for t in otherTiles:
                ix = (t.x - self.game.emptySpace[0]) // self.game.tileSize
                iy = (t.y - self.game.emptySpace[1]) // self.game.tileSize
                self.game.revealTile(int(ix), int(iy))
                didSomething = True
        return didSomething
