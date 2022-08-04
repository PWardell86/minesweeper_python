import unittest
from src.game.utils import TileUtils


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.SIMPLELIST = TileUtils.generateRandomTiles(1, 2)
        self.LISTLIST = TileUtils.generateRandomTiles(2, 2)


if __name__ == '__main__':
    unittest.main()
