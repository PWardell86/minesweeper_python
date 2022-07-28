from MinesweeperMVC import Minesweeper
from src.bot.SimpleBot import SimpleBot
from pyglet import app, gl, clock
playWithBot = True

game = Minesweeper(gameSize=(20, 15))
if playWithBot:
    bot = SimpleBot(game)
    bot.start()
    clock.schedule_interval(bot.tick, 1)

# Remove aliasing
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

app.run()
