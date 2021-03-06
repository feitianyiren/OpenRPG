import unittest
import sys
import os
from shutil import rmtree

sys.path.insert(0, '../OpenRPG')
from OpenRPG.Game import Game
from OpenRPG.Level import Level
from OpenRPG.util import dirExists, _clock

Game.GAMES_DIRECTORY = './tmp'


# Magically make unit tests deterministic
_clock.setMock(True)

class test_Level(unittest.TestCase):
    def test_init_delete(self):
        parentGame = Game()
        level = Level(None, parentGame)
        level2 = Level(level.name, parentGame)

        self.assertTrue(os.path.exists(level.getDir()))
        self.assertTrue(os.path.exists(level.getFloorplanPath()))

        for key in level.__dict__:
            self.assertTrue(key in level2.__dict__)
            if key in level2.__dict__:
                self.assertEqual(level.__dict__[key], level2.__dict__[key])

        parentGame.delete()

        self.assertFalse(os.path.exists(level.getDir()))
        self.assertFalse(os.path.exists(level.getFloorplanPath()))

    def test_updateFloorplanImageId(self):
        parentGame = Game()
        level = Level(None, parentGame)

        oldId = level._floorplanImageID
        _clock.tick()
        level.updateFloorplanImageID()

        self.assertNotEqual(oldId, level._floorplanImageID)

        parentGame.delete()


if __name__ == '__main__':
    if not dirExists(Game.GAMES_DIRECTORY):
        os.mkdir(Game.GAMES_DIRECTORY)

    unittest.main()