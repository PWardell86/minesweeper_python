from pyglet import sprite, graphics
class Tile(sprite.Sprite):
    def __init__(self, x, y, size, defaultImage, batch, value=None, isRevealed=False, isFlagged=False):
        """
        Defines a tile for the game
            - isRevealed --> if the tile has been clicked / revealed
            - isFlagged --> if the tile is flagged
            - value --> what the value of the tile is: 
                - 0 - 8 are regular values
                - 9 is a bomb
        """
        self.isRevealed = isRevealed
        self.isFlagged = isFlagged
        self.value = value
        super(Tile, self).__init__(defaultImage, x, y, batch=batch, group=graphics.OrderedGroup(-1))
        
        # Scale the tile properly
        self.scale = size / self.width
