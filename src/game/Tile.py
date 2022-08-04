from pyglet import sprite, graphics


class Tile(sprite.Sprite):
    def __init__(self, x, y, size, index, defaultImage, batch, value=None):
        """
        Defines a tile as a sprite for minesweeper.
        Position is relative to the top left corner

        :param x: The x position of the tile, in pixels
        :param y: The y position of the tile, in pixels
        :param size: The size of the tile in pixels. The given image will be scaled
        :param defaultImage: The image to give to the tile when it is generated
        :param batch: Batch that the tile with belong to
        :param value: The tile's value. [0-9]: blank -> bomb
        """
        self.isRevealed = False
        self.isFlagged = False
        self.value = value
        super(Tile, self).__init__(defaultImage, x, y,
                                   batch=batch, group=graphics.OrderedGroup(-1))
        # Scale the tile properly
        self.scale = size / self.width
        self.nearTiles = []
        self.index = index

    def __str__(self):
        output = f"Value: {self.value}, {int(self.isFlagged)}, {int(self.isRevealed)}"
        return output

    def setNearTiles(self, tiles):
        self.nearTiles = tiles

    def getNearFlags(self):
        flags = 0
        for tile in self.nearTiles:
            if tile.isFlagged:
                flags += 1
        return flags
