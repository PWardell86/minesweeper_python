

class Bot:
    def __init__(self, game):
        self.game = game.minesweeperControl
        self.visual = game
        # A list of methods for each special case

        for method_name in dir(self):
            method = getattr(self, method_name)
            if callable(method):
                print(method.__annotations__)

        self.theseRules = [
        ]
        self.allRules = []
        self.didSomething = False

    def testOnlyCurrentLevelRules(self):
        self.allRules = self.theseRules

    def start(self):
        self.game.startGame(self.game.gameSize[0] // 2, self.game.gameSize[1] // 2)

    def tick(self, t):
        self.didSomething = False
        if self.game.gameOver:
            return
        if self.game.started:
            for row in self.game.tiles:
                for tile in row:
                    self.iterateCases(tile)
            if self.didSomething:
                print("Did something...")
            else:
                print("Done...")

            self.visual.update()

    def iterateCases(self, tile):
        for case in self.allRules:
            case(tile)

Bot(None)