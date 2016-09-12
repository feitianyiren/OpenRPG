'''
    
'''

import json
import os
import shutil
from util import *

class Level(Saveable, object):
    currentID = -1

    def __init__(self, name, directory):
        self.name = name
        self.directory = os.path.join(directory, self.name.replace(' ', '_'))
        self.ID = None
        self.width = 640
        self.height = 480

    def load(self):
        super(self.__class__, self).load()

        if self.ID > Level.currentID:
            Level.currentID = self.ID

    def delete(self):
        shutil.rmtree(self.getDir())

    def initFiles(self):
        self.ID = Level.getID()
        os.makedirs(self.directory)
        self.save()

    def getDir(self):
        return self.directory

    def getFloorplanPath(self):
        return os.path.join(self.getDir(), 'floorplan.png')

    @staticmethod
    def getID():
        Level.currentID += 1
        return Level.currentID