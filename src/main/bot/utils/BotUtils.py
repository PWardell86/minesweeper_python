from src.main.bot.IntermediateBot import IntermediateBot
from src.main.bot.SimpleBot import SimpleBot
from src.main.bot.SuperiorBot import SuperiorBot
from src.main.game import MinesweeperModelControl


def playWithBot(level: int, game: MinesweeperModelControl, clock, interval, testChanges=False):
    bot = None
    if level == 0:
        return
    if level == 1:
        bot = SimpleBot(game)
    elif level == 2:
        bot = IntermediateBot(game)
    elif level == 3:
        bot = SuperiorBot(game)

    if bot is not None:
        if testChanges:
            bot.testOnlyCurrentLevelRules()
            print(bot.allRules)
        bot.start()
        if interval is None:
            clock.schedule(bot.tick)
        else:
            clock.schedule_interval(bot.tick, interval)
