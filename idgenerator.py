


class IDgenerator():
    def __init__(self):

        self.count = 0
        self.prefix = "__"
    def getID(self):

        return self.prefix + str(self.count + 1)
