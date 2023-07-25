from pyglet import app, gl, clock
from src.main.game.MinesweeperModelControl import MinesweeperMC
from src.main.game.MinesweeperVisual import MinesweeperV
from src.main.bot.utils import BotUtils
from sys import argv
from src.main.utils.PropertiesUtils import PropertiesUtil

# Remove aliasing so the quality stays the same on zoom
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
config = PropertiesUtil("../defaults.properties")

def start_game(args_map):
    difficulty = config.getFloat("difficulty")
    bot_level = config.getInt("bot_level")
    game = MinesweeperV(
        theme=config.getStr("theme"),
        difficulty=difficulty,
        game_size=(config.getInt("game_width"), config.getInt("game_height")),
        dev=config.getBoolean("dev") or ("--dev" in args_map),
        window_size=(config.getInt("window_width"), config.getInt("window_height"))
    )
    if bot_level != 0:
        tick = BotUtils.playWithBot(bot_level, game, clock, difficulty)

def get_args_map():
    args_map = {}
    for arg in argv:
        keyValue = arg.split("=")
        if (len(keyValue) >= 2):
            args_map[keyValue[0]] = keyValue[1]
        elif (len(keyValue) == 1):
            args_map[keyValue[0]] = None
    return args_map
    
print(config.getBoolean("dev"), ("--dev" in get_args_map()))
args_map = get_args_map()
start_game(args_map)
app.run()
