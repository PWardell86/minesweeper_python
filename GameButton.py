from pyglet import sprite
class GameButton(sprite.Sprite):
    def __init__(self, x, y, restImage, pressedImage, width, height, command, batch):
        super(GameButton, self).__init__(restImage, x, y, batch=batch)
        self.batch = batch
        self.scale_x = width / self.width
        self.scale_y = height / self.height
        self.restImage = restImage
        self.pressedImage = pressedImage
        self.command = command

    def clickEvent(self, cx, cy, released):
        if (cx > self.x and cx < (self.x + self.width) and
                cy > self.y and cy < (self.y + self.height)):
            if released == 0:
                self.image = self.pressedImage
            if released == 1:
                self.image = self.restImage
                self.command()