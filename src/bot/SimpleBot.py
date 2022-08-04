from src.game.MinesweeperMVC import Minesweeper

from src.game.Tile import Tile


class SimpleBot:
    def __init__(self, game: Minesweeper):
        self.game = game
        # A list of methods for each special case
        # Must be methods that take no input
        self.theseRules = [
            self.revealAllTilesRule
            , self.flagAllTilesRule
        ]
        self.specialRules = self.theseRules

    def testOnlyCurrentLevelRules(self):
        self.specialRules = self.theseRules

    def start(self):
        self.game.startGame(self.game.gameSize[0] // 2, self.game.gameSize[1] // 2)

    def tick(self, t):
        if self.game.gameOver or self.game.resetting:
            return
        didSomething = False
        for row in self.game.tiles:
            for tile in row:
                self.iterateCases(tile)

        # if didSomething:
        #     print("Still solving...")
        # else:
        #     print("Done solving...")

    def iterateCases(self, tile):
        didSomething = False
        for case in self.specialRules:
            try:
                didSomething |= case(tile)
            except TypeError as e:
                print(e)

    def flagAllTilesRule(self, tile):
        didSomething = False
        if tile.isRevealed:
            didSomething |= self.flagNearTilesIfPossible(tile.nearTiles, tile)
        return didSomething

    def revealAllTilesRule(self, tile: Tile):
        didSomething = False
        if tile.isRevealed:
            didSomething |= self.revealNearTilesIfPossible(tile.nearTiles, tile)

        return didSomething

    def flagNearTilesIfPossible(self, nearTiles: list, tile):
        didSomething = False
        unrevealedTiles = 0
        flaggedTiles = 0
        otherTiles = []
        for t in nearTiles:
            if not t.isRevealed and not t.isFlagged:
                otherTiles.append(t)
                unrevealedTiles += 1
            elif t.isFlagged:
                flaggedTiles += 1

        if unrevealedTiles == tile.value - flaggedTiles:
            for t in otherTiles:
                self.game.flagTileFromTile(t)
                didSomething = True
        return didSomething

    def revealNearTilesIfPossible(self, tiles: list, tile):
        didSomething = False
        flaggedTiles = 0
        unrevealedTiles = []
        for t in tiles:
            if t.isFlagged:
                flaggedTiles += 1
            elif not t.isRevealed:
                unrevealedTiles.append(t)
                # If the number of flagged tiles == the value of the tile, we know that none of the unrevealed tiles can
                # be bombs. So we reveal them
        if flaggedTiles == tile.value:
            for t in unrevealedTiles:
                self.game.revealTileFromTile(t)
                didSomething = True
        return didSomething
