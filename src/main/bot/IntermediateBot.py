from src.main.bot.SimpleBot import SimpleBot
from src.main.utils import TileUtils

class IntermediateBot(SimpleBot):
    def __init__(self, game):
        super(IntermediateBot, self).__init__(game)
        self.theseRules = [
            self.two_near_one_rule,
            self.value_one_shares_all_near_tiles
        ]
        self.all_rules += self.theseRules

    def two_near_one_rule(self, tile):
        self.check_and_reveal_two_one_case(tile, tile.near_tiles)

    def value_one_shares_all_near_tiles(self, tile):
        self.check_one_shares_all_near_tiles_case(tile)

    def check_one_shares_all_near_tiles_case(self, tile):
        if tile.revealed:
            for nearTile in tile.near_tiles:
                # If all unrevealed tiles near this one are shared by another...
                common = TileUtils.getCommonTilesUnrevealedUnflagged(tile.near_tiles, nearTile.near_tiles)
                if common == TileUtils.getUnrevealed(tile.near_tiles, True):
                    certainNearBombs = tile.value - tile.get_near_flags()

                    if nearTile.value - nearTile.get_near_flags() - certainNearBombs == 0:
                        for revealTile in TileUtils.getNonCommonTiles(nearTile.near_tiles, tile.near_tiles, True):
                            self.did_something |= self.game.reveal_tile(revealTile.x, revealTile.y)
                        break

    def check_and_reveal_two_one_case(self, tile, near_tiles: list):
        # If we have a 2 beside a 1
        if tile.revealed and not tile.flagged and tile.value - tile.get_near_flags() == 2:
            for checkTile in near_tiles:
                if checkTile.value - checkTile.get_near_flags() == 1:
                    # Get the tiles that are around the 2 value and not the 1 value
                    onlyNearTwoValue = TileUtils.getNonCommonTiles(near_tiles, checkTile.near_tiles, True)
                    # Of those tiles, get the ones that are not flagged
                    unflagged = TileUtils.getUnflagged(onlyNearTwoValue, checkRevealed=True)
                    # If there is only one unrevealed, unflagged tile near the 2 then it must be a bomb
                    if len(unflagged) == 1:
                        unflagged = unflagged[0]
                        self.game.flag_tile(unflagged.x, unflagged.y)
                        self.did_something = True
                        onlyNearOneValue = TileUtils.getNonCommonTiles(checkTile.near_tiles, near_tiles, True)
                        for revealTile in onlyNearOneValue:
                            if not revealTile.flagged:
                                self.did_something |= self.game.reveal_tile(revealTile.x, revealTile.y)
                        # Once we have placed flags and revealed tiles we have to stop because our previous data is now
                        # bad
                        break
