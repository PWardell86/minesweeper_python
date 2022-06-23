from pyglet import text, graphics, clock

class Counter(text.Label):
    def __init__(self, x, y, batch, initial=0, font="Joystix Monospace", fontSize=20, color=(0, 200, 0, 255)):
        super(Counter, self).__init__(
            str(initial),
            font_name=font, font_size=fontSize, color=color,
            anchor_x="center", anchor_y="center", x=x, y=y,
            batch=batch, group=graphics.OrderedGroup(2))  # Move it to the top so it can be seen
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
    def __init__(self, x, y, batch, initial=0, font="Joystix Monospace", fontSize=20, color=(0, 200, 0, 255)):
        super(Timer, self).__init__(x, y, batch, initial, font, fontSize, color)
        clock.schedule_interval(lambda t: self.plus(), 1)
