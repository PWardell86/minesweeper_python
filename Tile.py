from pyglet import sprite
class Tile(sprite.Sprite):
    def __init__(self, x, y, size, defaultImage, batch, value=None, isRevealed=False, isFlagged=False):
        self.isRevealed = isRevealed
        self.isFlagged = isFlagged
        self.value = value
        # defaultImage.anchor_x = defaultImage.width / 2
        # defaultImage.anchor_y = defaultImage.height / 2
        super(Tile, self).__init__(defaultImage, x, y, batch=batch)
        
        # Scale the tile properly
        self.scale = size / self.width
