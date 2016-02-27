##### REFACTORING STATUS #####
# X,Y,G,H,F A RENOMMER

class Cellule():

    def __init__(self, x, y, atteignable):
        self.atteignable = atteignable
        self.x = x
        self.y = y
        self.parent = None
        self.poid = 0
        self.h = 0
        self.priorite = 0

    def getHeuristic(self, arriver):
        return 10 * (abs(self.x - arriver.x) + abs(self.y - arriver.y))