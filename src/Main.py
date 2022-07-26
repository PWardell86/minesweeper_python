from MinesweeperMVC import Minesweeper
from pyglet import app, gl

game = Minesweeper(gameSize=(20, 15))

# Remove aliasing
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

app.run()
