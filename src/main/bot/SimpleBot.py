from src.main.bot.Bot import Bot


class SimpleBot(Bot):
    def __init__(self, game):
        super(SimpleBot, self).__init__(game)
        # A list of methods for each special case
        # Must be methods that take no input
        self.theseRules = [
            self.revealAllTilesRule, 
            self.flagAllTilesRule
        ]
        self.allRules += self.theseRules

    def flagAllTilesRule(self, tile):
        if tile.revealed:
            self.flagNearTilesIfPossible(tile.nearTiles, tile)

    def revealAllTilesRule(self, tile):
        if tile.revealed:
            self.revealNearTilesIfPossible(tile.nearTiles, tile)

    def flagNearTilesIfPossible(self, nearTiles: list, tile):
        unrevealedTiles = 0
        flaggedTiles = 0
        otherTiles = []
        for t in nearTiles:
            if not t.revealed and not t.flagged:
                otherTiles.append(t)
                unrevealedTiles += 1
            elif t.flagged:
                flaggedTiles += 1

        if unrevealedTiles == tile.value - flaggedTiles:
            for t in otherTiles:
                self.game.flagTile(t.x, t.y)
                self.didSomething = True

    def revealNearTilesIfPossible(self, tiles: list, tile):
        flaggedTiles = 0
        unrevealedTiles = []
        for t in tiles:
            if t.flagged:
                flaggedTiles += 1
            elif not t.revealed:
                unrevealedTiles.append(t)
                # If the number of flagged tiles == the value of the tile, we know that none of the unrevealed tiles can
                # be bombs. So we reveal them
        if flaggedTiles == tile.value:
            for t in unrevealedTiles:
                self.didSomething |= self.game.revealTile(t.x, t.y)
