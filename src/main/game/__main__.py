from pyglet import app, gl, clock
from src.main.game.MinesweeperVisual import MinesweeperV
from src.main.bot.utils import BotUtils


BOT_LEVEL = 0

game = MinesweeperV(difficulty=0.25, gameSize=(20, 15))
tick = BotUtils.playWithBot(BOT_LEVEL, game, clock, 1, False)

# Remove aliasing so the quality stays the same
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

app.run()
