from pyglet import graphics, resource, sprite


class Button(sprite.Sprite):
    def __init__(self, parent, index, rest_image, press_image, theme_dir, batch, command):
        size = parent.height / 1.5
        y_off = (parent.height / 2) - (size / 2) + parent.y
        x_off = (parent.width / 2) - (size + 4) * index + parent.x
        self.rest_image = resource.image(f"{theme_dir}/{rest_image}")
        self.press_image = resource.image(f"{theme_dir}/{press_image}")
        super(Button, self).__init__(self.rest_image, x=x_off, y=y_off,
                                    batch=batch, group=graphics.OrderedGroup(2))
        self.scale_x = size / self.width
        self.scale_y = size / self.height
        
        self.command = lambda: command()

    def click_event(self, cx, cy, released):
        if self.x < cx < self.x + self.width and self.y < cy < self.y + self.height:
            if released == 0:
                self.image = self.press_image
            else:
                self.image = self.rest_image
                self.command()
