
class Gruppe:
    def __init__(self, roboter, start, x, y):

        self.roboter = roboter
        self.head = roboter[0] if roboter else None
        self.role = 'Head'
        self.anzahl = len(roboter)
        self.color = 'white'
        #self.color = "rgba(0, 0, 0, 0)"

        self.current = start
        self.target = start
        self.x = x
        self.y = y



    def getColor(self):
        return self.color

    def getName(self):
        return self.head.name

    def print(self):
        print(self.head.name, ": Anzahl=", self.anzahl)