from src.main.bot.IntermediateBot import IntermediateBot
from src.main.bot.SimpleBot import SimpleBot
from src.main.bot.SuperiorBot import SuperiorBot
from src.main.game import MinesweeperModelControl

BOTS = {1: SimpleBot,
        2: IntermediateBot,
        3: SuperiorBot
        }

NUMBER_OF_BOTS = len(BOTS)


def playWithBot(level: int, game: MinesweeperModelControl, clock, interval: int, testChanges=False):
    try:
        bot = BOTS[int(level)](game)
    except KeyError:
        # TODO: Add logging
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
