from main.bot.Bot import Bot

class SimpleBot(Bot):
    def __init__(self, game):
        super(SimpleBot, self).__init__(game)
        # A list of methods for each special case
        # Must be methods that take no input
        self.theseRules = [
            self.revealAllTilesRule, 
            self.flagAllTilesRule
        ]
        self.all_rules += self.theseRules

    def flagAllTilesRule(self, tile):
        if tile.revealed:
            self.flag_near_tiles_if_possible(tile.near_tiles, tile)

    def revealAllTilesRule(self, tile):
        if tile.revealed:
            self.reveal_near_tiles_if_possible(tile.near_tiles, tile)

    def flag_near_tiles_if_possible(self, near_tiles: list, tile):
        unrevealedTiles = 0
        flaggedTiles = 0
        otherTiles = []
        for t in near_tiles:
            if not t.revealed and not t.flagged:
                otherTiles.append(t)
                unrevealedTiles += 1
            elif t.flagged:
                flaggedTiles += 1

        if unrevealedTiles == tile.value - flaggedTiles:
            for t in otherTiles:
                self.game.flag_tile(t.x, t.y)
                self.didSomething = True

    def reveal_near_tiles_if_possible(self, tiles: list, tile):
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
                self.didSomething |= self.game.reveal_tile(t.x, t.y)
