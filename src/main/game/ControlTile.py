class ControlTile:
    def __init__(self, x, y, index, value=None, near_tiles=None):
        self.x = x
        self.y = y
        self.index = index
        self.value = value
        self.flagged = False
        self.revealed = False
        self.near_tiles = near_tiles
        self.updated = False

    def set_near_tiles(self, near_tiles):
        self.near_tiles = near_tiles

    def get_near_flags(self):
        flags = 0
        try:
            for tile in self.near_tiles:
                if tile.flagged:
                    flags += 1
        except TypeError as e:
            print(self)
            raise e
        return flags

    def __str__(self):
        output = f"({self.x}, {self.y}), V: {self.value}, F: {self.flagged}, R: {self.revealed}"
        return output

    def mark_to_update(self):
        self.updated = False


