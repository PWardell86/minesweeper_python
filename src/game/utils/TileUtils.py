from random import randint

from pyglet import resource

from src.game.Tile import Tile
TEST_PATH = "utils/resources/testBlank.png"
TEST_IMAGE = resource.image(TEST_PATH)


def generateDummyTiles(rows: int, columns: int):
    dummyTiles = []
    for rowIndex in range(rows):
        row = []
        for columnIndex in range(columns):
            row.append(Tile(0, 0, 0, TEST_IMAGE, None, None))
        dummyTiles.append(row)
    return dummyTiles


def generateRandomTiles(rows: int, columns: int):
    randomTiles = []
    for rowIndex in range(rows):
        row = []
        for columnIndex in range(columns):
            row.append(Tile(0, 0, 0, TEST_IMAGE, None, randint(0, 9)))
        randomTiles.append(row)
    return randomTiles


def getColumn(column: int, tiles: list):
    newColumn = []
    for row in tiles:
        newColumn.append(row[column])


def toValueList(tiles: list):
    newList = []
    for tile in tiles:
        if tile is not list:
            newList.append(tile.value)
        else:
            newList.append(toValueList(tile))
    return newList


def toValueListMarkUnrevealed(tiles: list):
    newList = []
    for tile in tiles:
        if tile is not list:
            if not tile.isRevealed:
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
                if not tile0.isRevealed:
                    common.append(tile0)
            else:
                common.append(tile0)
    return common

def getCommonTilesUnrevealedUnflagged(tileGroup0, tileGroup1):
    common = []
    for tile0 in tileGroup0:
        if tile0 in tileGroup1:
            if not tile0.isRevealed and not tile0.isFlagged:
                common.append(tile0)
    return common

def getNonCommonTiles(tileGroup0, tileGroup1, checkRevealed=False):
    """
    Will give tiles in tileGroup0 that are not in tileGroup1
    :param tileGroup0: The first group of tiles
    :param tileGroup1: The second group of tiles
    :return: The tiles in tileGroup0 that are not in tileGroup1
    """
    uncommon = []
    for tile0 in tileGroup0:
        if tile0 not in tileGroup1:
            if checkRevealed:
                if not tile0.isRevealed:
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
        if not tile.isFlagged:
            if checkRevealed:
                if not tile.isRevealed:
                    notFlagged.append(tile)
            else:
                notFlagged.append(tile)
    return notFlagged

def getUnrevealed(tiles, checkFlagged=False):
    notFlagged = []
    for tile in tiles:
        if not tile.isRevealed:
            if checkFlagged:
                if not tile.isFlagged:
                    notFlagged.append(tile)
            else:
                notFlagged.append(tile)
    return notFlagged

