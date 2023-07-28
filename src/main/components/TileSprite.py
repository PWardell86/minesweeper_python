from pyglet import graphics, sprite


class TileSprite(sprite.Sprite):
    def __init__(self, x, y, size, defaultImage, batch):
        """
        Defines a tile as a sprite for minesweeper.
        Position is relative to the top left corner

        :param size: The size of the tile in pixels. The given image will be scaled
        :param defaultImage: The image to give to the tile when it is generated
        :param batch: Batch that the tile with belong to
        """

        super(TileSprite, self).__init__(defaultImage, x, y,
                                         batch=batch, group=graphics.OrderedGroup(-1))
        # Scale the tile properly
        self.scale = size / self.width

    def __str__(self):
        return str(self.image)

