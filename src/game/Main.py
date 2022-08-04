from MinesweeperMVC import Minesweeper
from src.bot.utils import BotUtils
from pyglet import app, gl, clock

BOT_LEVEL = 2

game = Minesweeper(difficulty=0.16, gameSize=(20, 15))
tick = BotUtils.playWithBot(BOT_LEVEL, game, clock, None, True)

# Remove aliasing
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

app.run()
