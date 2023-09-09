from pyglet import graphics, resource, sprite, image


class Button(sprite.Sprite):
    def __init__(self, parent, index, icon, theme_dir, batch, command):
        rest, pressed = "button-rest.png", "button-press.png"
        size = parent.height / 1.5
        y_off = (parent.height / 2) - (size / 2) + parent.y
        x_off = (parent.width / 2) - (size + 4) * index + parent.x
        self.rest_image = resource.image(f"{theme_dir}/{rest}")
        self.press_image = resource.image(f"{theme_dir}/{pressed}")
        super(Button, self).__init__(self.rest_image, x=x_off, y=y_off,
                                    batch=batch, group=graphics.OrderedGroup(2))
        self.icon_image = resource.image(f"{theme_dir}/{icon}")
        self.icon_sprite = sprite.Sprite(self.icon_image, x_off, y_off, batch=batch, group=graphics.OrderedGroup(3))
        self.scale_x, self.scale_y = size / self.width, size / self.height
        self.icon_sprite.scale_x, self.icon_sprite.scale_y = self.scale_x, self.scale_y
        self.command = command

    def click_event(self, cx, cy, released):
        if self.x < cx < self.x + self.width and self.y < cy < self.y + self.height:
            if released == 0:
                self.image = self.press_image
            else:
                self.image = self.rest_image
                self.command()
