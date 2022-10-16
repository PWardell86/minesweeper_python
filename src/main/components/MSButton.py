import pyglet.resource
from pyglet import sprite, graphics


class Button(sprite.Sprite):
    def __init__(self, x, y, restImage, pressedImage, width, height, batch, command, *args):
        super(Button, self).__init__(restImage, x, y,
                                    batch=batch, group=graphics.OrderedGroup(2))
        self.batch = batch
        self.scale_x = width / self.width
        self.scale_y = height / self.height
        self.restImage = restImage
        self.pressedImage = pressedImage
        self.command = lambda: command(*args)

    def clickEvent(self, cx, cy, released):
        if self.x < cx < self.x + self.width and self.y < cy < self.y + self.height:
            if released == 0:
                self.image = self.pressedImage
            if released == 1:
                self.image = self.restImage
                self.command()
