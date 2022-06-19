from MinesweeperGUI import Minesweeper
from pyglet import *
game = Minesweeper(gameSize=(20, 15))

global offset, initial_scale
initial_scale = game.tiles[0][0].scale
offset = [0, 0]
# Remove aliasing
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)


@game.event
def on_mouse_release(x, y, b, m):
    # Get mouse coordinates on the board
    real_tile_size = game.tileSize / (game.tiles[0][0].scale / initial_scale)
    posX = int((x - game.emptySpace[0]) / real_tile_size)
    posY = int((y - game.emptySpace[1]) / real_tile_size)

    # Check if the mouse is in the top bar
    game.btnSettings.clickEvent(x, y, 1)
    game.btnNewGame.clickEvent(x, y, 1)
    if (posX >= 0 and posX < game.gameSize[0]) and (posY >= 0 and posY < game.gameSize[1]):
        # Place a flag on the tile if key 4 is pressed (right click)
        if b == 4:
            game.flagTile(posX, posY)

        elif b == 1:  # Reveal the tile if key 1 is pressed (left click)
            if game.started:  # Check if the game has started and start it if not
                game.clickTile(posX, posY)
            else:
                game.startGame(posX, posY)


@game.event
def on_mouse_scroll(x, y, dx, dy):
    MAX_ZOOM = 5
    MIN_ZOOM = 1
    xZoomTo = int((x / game.width) * len(game.tiles[0]))
    yZoomTo = int((y / game.height) * len(game.tiles))

    for idy, row in enumerate(game.tiles):
        for idx, tile in enumerate(row):
            pdy = idy - yZoomTo
            pdx = idx - xZoomTo
            oldWidth = tile.width
            oldHeight = tile.height

            tile.scale = min(MAX_ZOOM,
                             max(MIN_ZOOM, tile.scale + (dy))
                             )
            tile.x -= pdx * (oldWidth - tile.width)
            tile.y -= pdy * (oldHeight - tile.height)


@game.event
def on_mouse_press(x, y, b, m):
    game.btnSettings.clickEvent(x, y, 0)
    game.btnNewGame.clickEvent(x, y, 0)


clock.schedule_interval(lambda t: game.cntTimer.plus(), 1)
app.run()
