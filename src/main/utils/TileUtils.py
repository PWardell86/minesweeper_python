from sys import path

from pyglet import resource

from main.components.ControlTile import ControlTile

TEST_PATH = "test/testBlank.png"
TEST_IMAGE = resource.image(TEST_PATH)

class TileSet(list):
    def forAll(self, f, **kwargs):
        for row in self:
            for tile in row:
                f(tile, **kwargs)

    def getTileAtIndex(self, index):
        x = index // len(self)
        y = index % len(self[0])
        return self[y][x]

    def getTileAtCoord(self, x, y):
        return self[y][x]

    def getTileFromTile(self, tile):
        return self.getTileAtIndex(tile.index)

    def getFlaggedCount(self):
        count = 0
        for row in self:
            for tile in row:
                if tile.flagged:
                    count += 1
        return count


def generateDummyTiles(rows: int, columns: int):
    dummyTiles = []
    for y in range(rows):
        row = []
        for x in range(columns):
            row.append(ControlTile(x, y, 0))
        dummyTiles.append(row)
    return dummyTiles


def getColumn(column: int, tileSet: TileSet):
    newColumn = []
    for row in tileSet:
        newColumn.append(row[column])


def toValueList(tileSet: TileSet):
    newList = []
    for tile in tileSet:
        if tile is not list:
            newList.append(tile.value)
        else:
            newList.append(toValueList(tile))
    return newList


def toValueListMarkUnrevealed(tileSet: TileSet):
    newList = []
    for tile in tileSet:
        if tile is not list:
            if not tile.visible:
                newList.append(None)
            else: newList.append(tile.value)
        else:
            newList.append(toValueListMarkUnrevealed(tile))
    return newList


def getCommonTiles(tileGroup0, tileGroup1, checkUnrevealed=False):
    common = []
    for tile0 in tileGroup0:
        if tile0 in tileGroup1:
            if checkUnrevealed:
                if not tile0.visible:
                    common.append(tile0)
            else:
                common.append(tile0)
    return common


def getCommonTilesUnrevealedUnflagged(tileGroup0, tileGroup1):
    common = []
    for tile0 in tileGroup0:
        if tile0 in tileGroup1:
            if not tile0.revealed and not tile0.flagged:
                common.append(tile0)
    return common


def getNonCommonTiles(tileGroup0, tileGroup1, checkRevealed=False):
    """
    Will give tiles in tileGroup0 that are not in tileGroup1
    :param checkRevealed:
    :param tileGroup0: The first group of tiles
    :param tileGroup1: The second group of tiles
    :return: The tiles in tileGroup0 that are not in tileGroup1
    """
    uncommon = []
    for tile0 in tileGroup0:
        if tile0 not in tileGroup1:
            if checkRevealed:
                if not tile0.revealed:
                    uncommon.append(tile0)
            else:
                uncommon.append(tile0)
    return uncommon


def getPrettyTileList(tiles: list):
    newList = []
    for tile in tiles:
        newList.append(str(tile))
    return newList


def getUnflagged(tiles, checkRevealed=False):
    notFlagged = []
    for tile in tiles:
        if not tile.flagged:
            if checkRevealed:
                if not tile.revealed:
                    notFlagged.append(tile)
            else:
                notFlagged.append(tile)
    return notFlagged


def getUnrevealed(tiles, checkFlagged=False):
    unrevealed = []
    for tile in tiles:
        if not tile.revealed:
            if checkFlagged:
                if not tile.flagged:
                    unrevealed.append(tile)
            else:
                unrevealed.append(tile)
    return unrevealed

