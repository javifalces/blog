import sys


####Cash Should be like an interface!
class Strategy:
    name = 'DefaultName'

    def init(self, dictionaryParameters, trainSet=None):
        print 'Must override it!'
        raise Exception('Must override init method!')

    def onBar(self, bar):
        print 'Must override it!'
        raise Exception('Must override init method!')
