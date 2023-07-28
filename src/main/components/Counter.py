from pyglet import clock, font, graphics
from pyglet.text import Label


class Counter(Label):
    def __init__(self, x, y, theme_dir, batch, initial=0, font_name="7 Segments", font_size=15, colour=(0, 200, 0, 255)):
        super(Counter, self).__init__(
            str(initial),
            font_name=font_name, font_size=font_size, color=colour,
            anchor_x="center", anchor_y="center", x=x, y=y,
            batch=batch, group=graphics.OrderedGroup(2))  # Move it to the top, so it can always be seen
        self.locked = False
        self.count = initial

    def plus(self):
        if self.locked:
            return
        self.count += 1
        self.text = str(self.count)

    def minus(self):
        if self.locked:
            return
        self.count -= 1
        self.text = str(self.count)

    def setCounter(self, count):
        if self.locked:
            return
        self.count = count
        self.text = str(count)


class Timer(Counter):
    """
    This time will be locked by default, but when unlocked it will count up on its own, once per second.
    There is no need to control it manually
    """
    def __init__(self, x, y, theme_dir, batch):
        super(Timer, self).__init__(x, y, theme_dir, batch)
        clock.schedule_interval(lambda t: self.plus(), 1)
