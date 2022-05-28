from pyglet import text
class Counter(text.Label):
    def __init__(self, x, y, batch, initial = 0, font = "Joystix Monospace", fontSize = 20, color = (0, 200, 0, 255)):
        super(Counter, self).__init__(
            str(initial),
            font_name = font, font_size = fontSize, color = color, 
            anchor_x = "center", anchor_y = "center", x = x, y = y, 
            batch = batch)
        self.count = initial
    
    def plus(self):
        self.count += 1
        self.text = str(self.count)
        
    def minus(self):
        self.count -= 1
        self.text = str(self.count)

    def setCounter(self, count):
        self.count = count
        self.text = str(count)
