import src.bot.SimpleBot
from src.bot.utils import BotUtils
from src.game.MinesweeperMVC import Minesweeper
from src.game.utils import TileUtils

class IntermediateBot(src.bot.SimpleBot.SimpleBot):
    def __init__(self, game: Minesweeper):
        super(IntermediateBot, self).__init__(game)
        self.theseRules = [self.twoNearOneRule, self.valueOneSharesAllNearTilesRule]
        self.specialRules += self.theseRules

    def twoNearOneRule(self, tile):
        return self.checkAndRevealTwoOneCase(tile, tile.nearTiles)

    def valueOneSharesAllNearTilesRule(self, tile):
        return self.checkOneSharesAllNearTilesCase(tile)

    def checkOneSharesAllNearTilesCase(self, tile):
        didSomething = False
        if tile.isRevealed:
            for nearTile in tile.nearTiles:
                # If all unrevealed tiles near this one are shared by another...
                common = TileUtils.getCommonTilesUnrevealedUnflagged(tile.nearTiles, nearTile.nearTiles)
                if common == TileUtils.getUnrevealed(tile.nearTiles, True):
                    # print(f"Hit: ({tile.index[0]}, {tile.index[1]})")
                    certainNearBombs = tile.value - tile.getNearFlags()

                    if nearTile.value - nearTile.getNearFlags() - certainNearBombs == 0:
                        for revealTile in TileUtils.getNonCommonTiles(nearTile.nearTiles, tile.nearTiles, True):
                            self.game.revealTileFromTile(revealTile)
                        break
        return didSomething

    def checkAndRevealTwoOneCase(self, tile, nearTiles: list):
        didSomething = False
        # If we have a 2 beside a 1
        if tile.isRevealed and not tile.isFlagged and tile.value - tile.getNearFlags() == 2:
            for checkTile in nearTiles:
                if checkTile.value - checkTile.getNearFlags() == 1:
                    # Get the tiles that are around the 2 value and not the 1 value
                    onlyNearTwoValue = TileUtils.getNonCommonTiles(nearTiles, checkTile.nearTiles, True)
                    # Of those tiles, get the ones that are not flagged
                    unflagged = TileUtils.getUnflagged(onlyNearTwoValue, checkRevealed=True)
                    # If there is only one unrevealed, unflagged tile near the 2 then it must be a bomb
                    if len(unflagged) == 1:
                        # Works when this is commented out
                        self.game.flagTileFromTile(unflagged[0])
                        didSomething = True
                        onlyNearOneValue = TileUtils.getNonCommonTiles(checkTile.nearTiles, nearTiles, True)
                        for revealTile in onlyNearOneValue:
                            if not revealTile.isFlagged:
                                self.game.revealTileFromTile(revealTile)
                        # Once we have placed flags and revealed tiles we have to stop because our previous data is now
                        # bad
                        break
        return didSomething