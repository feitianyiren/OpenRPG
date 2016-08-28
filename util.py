import os, json

class Saveable:
    '''
        Enables derived classes to save their __dict__s as JSON
        Important for git compatibility
    '''
    def getSaveFilePath(self):
        return os.path.join(self.directory, 'config.json')

    def save(self):
        '''
            Save JSON metadata
        '''
        try:
            f = open(self.getSaveFilePath(), 'w')
            f.write(json.dumps(self, indent=3, cls=DictEncoder, sort_keys=True))
            f.close()
        except IOError as e:
            print e

    def load(self):
        '''
            Load metadata from self.directory
        '''
        try:
            f = open(self.getSaveFilePath(), 'r')
            values = json.load(f)
            mustSave = False

            for key in self.__dict__:
                if not key in values:
                    # A new key has been added
                    # Save to bring legacy data up to date
                    mustSave = True

            for key in values:
                self.__dict__[key] = values[key] 

            f.close()

            if mustSave:
                self.save()

        except IOError as e:
            print e

class DictEncoder(json.JSONEncoder):
    '''
        Enables the encoding of arbitrary Python objects to JSON
    '''
    def default(self, o):
        return o.__dict__

def dirExists(path):
    '''
        Returns true if a directory exists
    '''
    return os.path.exists(path) and os.path.isdir(path)
