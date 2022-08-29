class ControlTile:
    def __init__(self, x, y, index, value=None, nearTiles=None):
        self.x = x
        self.y = y
        self.index = index
        self.value = value
        self.flagged = False
        self.revealed = False
        self.nearTiles = nearTiles
        self.updated = False

    def setNearTiles(self, nearTiles):
        self.nearTiles = nearTiles

    def getNearFlags(self):
        flags = 0
        try:
            for tile in self.nearTiles:
                if tile.flagged:
                    flags += 1
        except TypeError as e:
            print(self)
            raise e
        return flags

    def __str__(self):
        output = f"Value: ({self.x}, {self.y}), V: {self.value}, F: {self.flagged}, R: {self.revealed}"
        return output

    def markToUpdate(self):
        self.updated = False


