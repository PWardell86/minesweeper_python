from pyglet import graphics, resource, sprite


class TopBar(sprite.Sprite):
    def __init__(self, parent, theme_dir, batch):
        super(TopBar, self).__init__(resource.image(
            f"{theme_dir}/TopBar.png"), batch=batch, group=graphics.OrderedGroup(1))
        self.theme_dir = theme_dir
        self.y = parent.height - self.height
        self.scale_x = parent.width / self.width

    def getHeight(self):
        return self.height