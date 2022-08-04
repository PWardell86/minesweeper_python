from src.bot.IntermediateBot import IntermediateBot
from src.bot.SimpleBot import SimpleBot
from src.game.MinesweeperMVC import Minesweeper


def playWithBot(level: int, game: Minesweeper, clock, interval, testChanges=False):
    bot = None
    if level == 0:
        return
    if level == 1:
        bot = SimpleBot(game)
    elif level == 2:
        bot = IntermediateBot(game)

    if bot is not None:
        if testChanges:
            bot.testOnlyCurrentLevelRules()
        bot.start()
        if interval is None:
            clock.schedule(bot.tick)
        else:
            clock.schedule_interval(bot.tick, interval)
