class Bot:
    def __init__(self, game):
        self.game = game.minesweeper_control
        self.visual = game
        # A list of methods for each special case

        self.these_rules = []
        self.all_rules = []
        self.did_something = False

    def only_test_current_level_rules(self):
        self.all_rules = self.these_rules

    def start(self):
        self.game.start_game(self.game.game_size[0] // 2, self.game.game_size[1] // 2)

    def tick(self, t):
        if self.game.game_over:
            return
        if self.game.started:
            self.did_something = False
            self.game.for_tiles(self.iterate_cases)
            if self.did_something:
                print("Working...")
            self.visual.update()

    def iterate_cases(self, tile):
        for rule in self.all_rules:
            rule(tile)
