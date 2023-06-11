from pyglet import app, gl, clock
from src.main.game.MinesweeperModelControl import MinesweeperMC
from src.main.game.MinesweeperVisual import MinesweeperV
from src.main.bot.utils import BotUtils
from sys import argv

def startGame(difficulty, gameSize, bot_level, dev=False):
    game = MinesweeperV(difficulty=difficulty, gameSize=gameSize, dev=dev)
    if bot_level != 0:
        print(bot_level)
        tick = BotUtils.playWithBot(bot_level, game, clock, 0.16, False)
        
# Remove aliasing so the quality stays the same
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

# Take command line arguments and pass them to the game
botLevel = 0
argsMap = {}
for arg in argv:
    keyValue = arg.split("=")
    if (len(keyValue) >= 2):
        argsMap[keyValue[0]] = keyValue[1]
    elif (len(keyValue) == 1):
        argsMap[keyValue[0]] = None

if "--dev" in argsMap:
    print("In dev mode...")
if "--bot" in argsMap:
    print(f"With bot level: {argsMap['--bot']}...")
    botLevel = argsMap["--bot"]

startGame(0.16, (15, 20), bot_level)

app.run()
