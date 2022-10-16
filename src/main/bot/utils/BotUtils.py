from src.main.bot.IntermediateBot import IntermediateBot
from src.main.bot.SimpleBot import SimpleBot
from src.main.bot.SuperiorBot import SuperiorBot
from src.main.game import MinesweeperModelControl

NUMBER_OF_BOTS = 3
BOTS = {1: SimpleBot,
        2: IntermediateBot,
        3: SuperiorBot
        }


def playWithBot(level: int, game: MinesweeperModelControl, clock, interval, testChanges=False):
    try:
        bot = BOTS[level](game)
    except KeyError:
        bot = None

    if bot is not None:
        if testChanges:
            bot.testOnlyCurrentLevelRules()
            print(bot.allRules)
        bot.start()
        if interval is None:
            clock.schedule(bot.tick)
        else:
            clock.schedule_interval(bot.tick, interval)
